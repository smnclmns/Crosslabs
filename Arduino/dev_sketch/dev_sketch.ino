#include <Wire.h>
#include "Adafruit_AS726x.h"
#include "SpeedyStepper.h"
#include <Tic.h>
TicI2C tic;

// On boards with a hardware serial port available for use, use
// that port to communicate with the Tic. For other boards,
// create a SoftwareSerial object using pin 10 to receive (RX)
// and pin 11 to transmit (TX).

// Buffer to read the Serial port commands
String inputString = "";
bool stringComplete = false;
bool titrationCompletePrinted = false;

// Motor object, outputs and buffer variables
SpeedyStepper stepper;
const int MOTOR_STEP_PIN = 3;
const int MOTOR_DIRECTION_PIN = 4;
long NULLPOSITION = 0;
long ENDPOSITION = 11000; // number of steps from full to empty syringe
long POSITION = 0;
long margin;


// Lightsensor object and buffer
Adafruit_AS726x ams;
//buffer to hold Adafruit sensor raw values
uint16_t sensorValues[AS726x_NUM_CHANNELS];


// Titration adjustments and buffer
bool Start = false;
unsigned long Starttime = 0;
uint16_t currentTime;

// Phases of titration
/*
 * 0 ~ break
 * 1 ~ first phase (fastest)
 * 2 ~ second phase (medium fast)
 * 3 ~ last phase (slow)
 * 4 ~ finish
 */
// Titrationsphasen
boolean phase1 = false;
boolean phase2 = false;
boolean endphase = false;
boolean fertig = false;
boolean pause = false;
uint8_t phase = 0;

// Farbsensor Vergleichswerte 
int startvalues[6] = {0,0,0,0,0,0};
int values[6] = {0,0,0,0,0,0};

// Adjustments for the process
double change = 0.9; // indicates at what percentage of the initial intensity of a light value phase 2 should be initiated
double endvalue = 0.9; // indicates at what percentage of the initial intensity of a light value the titration should stop
double endtime = 8000.0; // waiting time in s to check if titration is finished
double steps1 = 1250.0 ; // indicates the number of steps in phase 1 after which the light values are compared
double steps2 = 650.0 ; // indicates the number of steps in phase 2 after which the light values are compared


void setup(void) {

  Serial.begin(9600);
  while(!Serial);

  pinMode(LED_BUILTIN, OUTPUT);

  if (!ams.begin()) {
    Serial.println("Could not connect to sensor! Please check your wiring.");
  }

  Serial.println("Light Sensor ready...");
  Wire.begin();
  delay(20);
  tic.setStepMode(TicStepMode::Microstep32);
  Serial.println("Stepper motor ready...");
  Serial.println("Margin:");
  margin = (1-change)*100;
  Serial.print(margin);Serial.print("%");
  tic.energize();
  tic.exitSafeStart();
  

}

//Loop Start  
void loop(void) {

      // Check for available serial data
  if (stringComplete) {
    Serial.print(inputString);

    /*
     * From here, commands are executed depending on the content of the Serial port.
     */

    if (inputString == "Start\n") {
      Starttime = millis();
      send_in_utf_8();

      //Declare starting Variables
      farbmessung();
      startvalues[0] = sensorValues[AS726x_VIOLET];
      startvalues[1] = sensorValues[AS726x_BLUE];
      startvalues[2] = sensorValues[AS726x_GREEN];
      startvalues[3] = sensorValues[AS726x_YELLOW];
      startvalues[4] = sensorValues[AS726x_ORANGE];
      startvalues[5] = sensorValues[AS726x_RED];
      //First measurement for the Plot
      farbmessung();
      send_in_utf_8();
      //set the starting point of the titration
      Serial.println("Automated Titration Started");
      //Initializing the Phase and Position
      tic.haltAndSetPosition(0);
      titrationCompletePrinted = false;
      pause=false;
      POSITION=0;
      phase1 = true;
      }
  

    else if (inputString == "mock\n") {
      Mocking_Data();
      
    }

    else if (inputString == "Stop\n") {
      phase1 = false;
      phase2 = false;
      endphase = false;
      Serial.println("Stop all actions");
    }

    else if (inputString == "Cali\n" && !Start) {
      Serial.println("Calibration started \nDo not forget to weight the fluid");
      Calibration();
    }

    else if (inputString == "Reset\n") {
      phase1 = false;
      phase2 = false;
      endphase = false;
      Reset();
    }
    else if (inputString == "Pause\n") {
      phase1 = false;
      phase2 = false;
      endphase = false;
      pause = true;
      Serial.println("Before you refill the Syringe switch the lever!");
      // Add a small delay and flush serial data
      delay(100);
      Serial.flush();
      
    }
    else if (inputString == "Refill\n") {
      Refill_Syringe();
    }
    else if (inputString == "Continue p1\n") {
      phase1 = true;
      phase2 = false;
      Serial.println("Continue with Phase 1");
    }

    else if (inputString == "Continue p2\n") {
      phase1 = false;
      phase2 = true;
      Serial.println("Continue with Phase 2");
    }

    else if (inputString.startsWith("f")) {
      tic.energize();
      tic.exitSafeStart();
      Serial.println("Forwardmovement for 1 second");   
      tic.setTargetVelocity(20000000);
      delayWhileResettingCommandTimeout(1000);
      tic.setTargetVelocity(0);
      delayWhileResettingCommandTimeout(2000);
      
        
    }

    else if (inputString.startsWith("b")) {
      tic.energize();
      tic.exitSafeStart();
      Serial.println("Backwardmovement for 1 second1"); 
      tic.setTargetVelocity(-20000000);
      delayWhileResettingCommandTimeout(1000);
      tic.setTargetVelocity(-0);
      delayWhileResettingCommandTimeout(2000);
    }

    else if (inputString.startsWith("long f")) {
      tic.energize();
      tic.exitSafeStart();
      Serial.println("Forwardmovement for 5 seconds");   
      tic.setTargetVelocity(80000000);
      delayWhileResettingCommandTimeout(5000);
      tic.setTargetVelocity(0);
      delayWhileResettingCommandTimeout(2000);
      
        
    }

    else if (inputString.startsWith("long b")) {
      tic.energize();
      tic.exitSafeStart();
      Serial.println("Backwardmovement for 5 seconds"); 
      tic.setTargetVelocity(-80000000);
      delayWhileResettingCommandTimeout(5000);
      tic.setTargetVelocity(-0);
      delayWhileResettingCommandTimeout(2000);
    }

    else if (inputString == "Null\n") {
      Serial.println("Nullpoint set");
      tic.haltAndSetPosition(0);
    }
    else if (inputString == "Change\n"){
      if (change == 0.9){
          change = 0.95;
          endvalue = 0.95;
          Serial.println("5 % Margin set");
        }
        else{
          change = 0.9;
          endvalue = 0.9;
          Serial.println("10 % Margin set");
        }
    }
    else if (inputString == "Test\n") {
      testFunction();
    } 

  delay(500);

    /*
   * End of command checking. 
   */

    inputString = "";
    stringComplete = false;
  }
  if (phase1){
    Serial.println("Phase 1");
    farbmessung();
    send_in_utf_8();
    for (int i=0;i<6;i++){
      if (values[i] < change*startvalues[i]){
        phase1 = false;
        phase2 = true;
      } // if Ende
    } // for Ende
    if (phase1){
      moving(steps1);
    } // if Ende
  } // if phase1 Ende

  // Sobald die Intensität eines beliebigen Farbwerts unter die festgelegte Schwelle fällt wird die nächste Phase aktiv

  // In Phase 2 wird nun vorsichtiger titriert, um den sensiblen Farbumschlag des Indikators zu erkennen
  
  else if (phase2){
    Serial.println("Phase 2");
    farbmessung();
    send_in_utf_8();
    for (int i=0;i<6;i++){
      if (values[i] < endvalue*startvalues[i]){
        phase2 = false;
        endphase = true;
      } // if Ende
    } // for Ende
    
    
    if (phase2){
      moving(steps2);
      Serial.println("Phase 2");
      
    } // if Ende
  } // else if phase2 Ende

// In der letzten Phase wird zu beginn eine gewisse Zeit gewartet, bevor erneut die Lichtwerte kontrolliert werden
// Damit auf die Situation reagiert werden, dass der Indikator sich wieder entfärbt hat

// Sollten  die Werte immernoch niedrig genug sein, wird die Titration gestoppt

  else if (endphase){
    Serial.println("Phase 3");
    farbmessung();
    send_in_utf_8();
    delay(15000);
    Serial.println("Extended Light Sensor Checking");
    farbmessung();
    send_in_utf_8();
    for (int i=0;i<6;i++){
      if (values[i] < endvalue*startvalues[i]){
        delay(500);
        farbmessung();
        send_in_utf_8();
        // Check if the message has not been printed before
        if (!titrationCompletePrinted) {
          farbmessung();
          send_in_utf_8();
          delay(500);
          Serial.println("Titration complete");
          Serial.print("\n");

          Serial.println("End position: ");
          Serial.println(POSITION);
          farbmessung();
          send_in_utf_8();

          // Set the variable to true to indicate that the message has been printed
          titrationCompletePrinted = true;
          endphase = false;
          Start = false;
          phase1 = false;
          phase2=false;
        }
      inputString ="Stop";
    
         
      } // if Ende
      
      if (endphase){
        endphase = false;
        phase2 = true;
      } // if Ende
      
     } // for Ende
  }

}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
      Serial.flush();
    }
  }
}

void moving(double x){
  //x steps in 1 second
  Serial.println("Moving...");
  tic.setTargetPosition(tic.getCurrentPosition() + x);
  delayWhileResettingCommandTimeout(1000);
  delayWhileResettingCommandTimeout(1000);
  tic.setTargetVelocity(0);
  delayWhileResettingCommandTimeout(1000);
  
  POSITION += x;
}

void liveticker(double x){
  String steps = String(x);
  Serial.println("s"+steps);
}

void Calibration() {
  tic.exitSafeStart();
  tic.setTargetVelocity(0);
  delayWhileResettingCommandTimeout(1000);
  int Cali_Position = 0;
  tic.setTargetPosition(tic.getCurrentPosition() + 20000);
  tic.exitSafeStart();
  delayWhileResettingCommandTimeout(5000);
  tic.setTargetVelocity(0);
  delayWhileResettingCommandTimeout(1000);
  delay(100);
  
  Serial.println("End of Calibration");
}

void Reset() {
    Serial.println("Pump moves to the Nullpoint and the Titration can be Started again");

    tic.exitSafeStart();
    tic.energize();
    if (pause){
      Serial.println("Because of the break inbetween the titration, the Syringe should be manually filled");
    }
  else{
      tic.setTargetPosition(tic.getCurrentPosition() - POSITION);
      delayWhileResettingCommandTimeout(POSITION * 2);
      tic.setTargetVelocity(0);
      delayWhileResettingCommandTimeout(1000);
      POSITION = 0;
      if (POSITION == 0){
        Serial.println("Already at the starting point");
      }
  }
    // Add a small delay and flush serial data
    delay(100);
    Serial.flush();
}

void Refill_Syringe() {
    Serial.println("Pump moves to the starting point");
    Serial.println("The Titrationprocess is only paused");

    tic.exitSafeStart();
    tic.energize();
    tic.setTargetPosition(tic.getCurrentPosition() - POSITION);
    delayWhileResettingCommandTimeout(POSITION * 2);
    tic.setTargetVelocity(0);
    delayWhileResettingCommandTimeout(1000);
    // Add a small delay and flush serial data
    delay(100);
    Serial.flush();
}


void farbmessung() {

  ams.startMeasurement();

  bool rdy = false;
  while(!rdy) {
    delay(100);
    rdy = ams.dataReady();
  }
  unsigned long millis_now = millis();
  long timediff = millis_now - Starttime;
  if (timediff >= 30000) {
  timediff -= 30000;
  Starttime += 30000;
  }
  currentTime = (uint16_t)timediff;

  ams.readRawValues(sensorValues);
  values[0] = sensorValues[AS726x_VIOLET];
  values[1] = sensorValues[AS726x_BLUE];
  values[2] = sensorValues[AS726x_GREEN];
  values[3] = sensorValues[AS726x_YELLOW];
  values[4] = sensorValues[AS726x_ORANGE];
  values[5] = sensorValues[AS726x_RED];
}


void livefarbe() {
    unsigned long millis_now = millis();
    long timediff = millis_now - Starttime;
    if (timediff >= 30000) {
    timediff -= 30000;
    Starttime += 30000;
    }
    currentTime = (uint16_t)timediff;
  
  if (sizeof(values) > 0) {
    String violet = String(values[0]);
    String blue = String(values[1]);
    String green = String(values[2]);
    String yellow = String(values[3]);
    String orange = String(values[4]);
    String red = String(values[5]);
    Serial.println(violet+","+blue+","+green+","+yellow+","+orange+","+red);
  }
}

void send_in_utf_8(){
  
  Serial.print(currentTime/10); Serial.print(",");
  
  for (uint8_t i=0; i<AS726x_NUM_CHANNELS; i++) {
     Serial.print(values[i]); Serial.print(",");
  }
  Serial.println();  
}
/*
 *  Mocking Data and Test Function
 */

void testFunction() {
  Serial.println("Test message received!");
  tic.setTargetVelocity(0);
  delayWhileResettingCommandTimeout(1000);
  Serial.println("Null Point Set");
  tic.haltAndSetPosition(0);
  tic.exitSafeStart();
  tic.setTargetPosition(2000);
  waitForPosition(2000);
  delayWhileResettingCommandTimeout(1000);
  Serial.println("Motor moved");
  tic.setTargetPosition(0);
  waitForPosition(2000);
  Serial.println("Going Home");
}

void Mocking_Data() {
  Serial.println("Lightsensor Test");
  for ( int i = 0; i<6;) { 
    farbmessung();
    send_in_utf_8();
    i +=1;
    delay(2000);
    }
  Serial.println("End of Test");
  
}



// Sends a "Reset command timeout" command to the Tic.  We must
// call this at least once per second, or else a command timeout
// error will happen.  The Tic's default command timeout period
// is 1000 ms, but it can be changed or disabled in the Tic
// Control Center
void resetCommandTimeout()
{
  tic.resetCommandTimeout();
}

// Delays for the specified number of milliseconds while
// resetting the Tic's command timeout so that its movement does
// not get interrupted.
void delayWhileResettingCommandTimeout(uint32_t ms)
{
  uint32_t start = millis();
  do
  {
    resetCommandTimeout();
  } while ((uint32_t)(millis() - start) <= ms);
}


// Polls the Tic, waiting for it to reach the specified target
// position.  Note that if the Tic detects an error, the Tic will
// probably go into safe-start mode and never reach its target
// position, so this function will loop infinitely.  If that
// happens, you will need to reset your Arduino.
void waitForPosition(int32_t targetPosition)
{
  do
  {
    resetCommandTimeout();
  } while (tic.getCurrentPosition() != targetPosition);
}
  
