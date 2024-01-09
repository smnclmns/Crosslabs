#include <Wire.h>
#include "Adafruit_AS726x.h"
#include "SpeedyStepper.h"

// Buffer to read the Serial port commands
String inputString = "";
bool stringComplete = false;

// Motor object, outputs and buffer variables
SpeedyStepper stepper;
const int MOTOR_STEP_PIN = 3;
const int MOTOR_DIRECTION_PIN = 4;
long NULLPOSITION = 0;
long ENDPOSITION = 11000; // number of steps from full to empty syringe
long POSITION = 0;


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
double endtime = 10.0; // waiting time in s to check if titration is finished
double steps1 = 50.0; // indicates the number of steps in phase 1 after which the light values are compared
double steps2 = 10.0; // indicates the number of steps in phase 2 after which the light values are compared

// Enables the generation of mocking data to test handling of sensor readings
bool mocking_data = false;


void setup(void) {

  Serial.begin(9600);
  while(!Serial);

  pinMode(LED_BUILTIN, OUTPUT);

  if (!ams.begin()) {
    Serial.println("Could not connect to sensor! Please check your wiring.");
  }

  stepper.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN); // implement the wiring of the motor


  Serial.println("Setup ready...");
}

  
void loop(void) {

  if (stringComplete) {
    Serial.print(inputString);

    /*
     * From here, commands are executed depending on the content of the Serial port.
     */

    if (inputString == "Start\n" && phase == 0 && !Start && !mocking_data) {
      Start = true;
      Starttime = millis();
      phase1 = true;
      Serial.println("Automated Titration Started");
    }

     // In Phase 1 werden zwischen den Lichtmessungen noch vergleichsweise viele Schritte ausgeführt, um die Zeit der Titration insgesamt zu verringern
  
  if (phase1){
    Serial.println("Phase 1");
    POSITION = 0;
    farbmessung();
    livefarbe();
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
    farbmessung();
    livefarbe();
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
    delay(endtime);
    farbmessung();
    livefarbe();
    for (int i=0;i<6;i++){
      if (values[i] < endvalue*startvalues[i]){
        endphase = false;
        Serial.println("Titration complete");
         
      } // if Ende
      
      if (endphase){
        endphase = false;
        phase2 = true;
      } // if Ende
      
    } // for Ende
  }


    else if (inputString == "mock\n" && !mocking_data && !Start) {
      mocking_data = true;
      Starttime = millis();
    }

    else if (inputString == "Stop\n") {
      Start = false;
      phase = 0;
      mocking_data = false;
      phase1 = false;
      phase2 = false;
      endphase = false;
      pause = true;
      Serial.println("Stop all actions");
    }

    else if (inputString == "Cali\n" && !Start) {
      Serial.println("Calibration started \nDo not forget to weight the fluid");
      Calibration();
    }

    else if (inputString == "Reset\n" && phase == 0) {
      Reset();
    }

    else if (inputString.startsWith("F")) {   
      stepper.setSpeedInRevolutionsPerSecond(10);
      stepper.setAccelerationInRevolutionsPerSecondPerSecond(10);
      stepper.moveRelativeInRevolutions(5);   
    }

    else if (inputString.startsWith("B")) {
      stepper.setSpeedInRevolutionsPerSecond(10);
      stepper.setAccelerationInRevolutionsPerSecondPerSecond(10.0);
      stepper.moveRelativeInRevolutions(-5);
    }

    else if (inputString == "Null\n") {
      Serial.println("Nullpoint set");
      NULLPOSITION = 0;
    }
    else if (inputString == "Change\n"){
      if (change=0.9){
          change = 0.95;
          endvalue = 0.95;
        }
        else{
          change = 0.9;
          endvalue = 0.9;
        }
    }
    else if (inputString == "Test\n") {
      testFunction();
    } 

  /*
   * End of command checking. 
   */

    inputString = "";
    stringComplete = false;
  }


   /*
    * Below the functions are executed in the loop depending on the current state.
    */

   

  if (Start == true) {
    send_in_utf_8();
    // Nachdem Befehle ausgeführt wurden wird mit der jeweiligen Phase fortgefahren

  // else if Ende
  }
  
  if (mocking_data && Start != true) {
    Mocking_Data();
    send_in_utf_8();
  }

  delay(1000);
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
  stepper.setSpeedInRevolutionsPerSecond(10.0);
  stepper.setAccelerationInRevolutionsPerSecondPerSecond(10.0);
  stepper.moveRelativeInSteps(x);
  if (x > 0){
    liveticker(x);
  } // if Ende
  NULLPOSITION += x;
  POSITION += x;
}

void liveticker(double x){
  String steps = String(x);
  Serial.println("s"+steps);
}

void Calibration() {
    stepper.setSpeedInRevolutionsPerSecond(10.0);
    stepper.setAccelerationInRevolutionsPerSecondPerSecond(10.0);
        for (int i=0;i<15;i++){
          stepper.moveRelativeInSteps(500);
          NULLPOSITION += 500;
          delay(1000);
        } // for
}

void Reset() {
    stepper.setSpeedInRevolutionsPerSecond(10);
    stepper.setAccelerationInRevolutionsPerSecondPerSecond(10);
    stepper.moveRelativeInSteps(-NULLPOSITION);
  
}

void Forward(long fw_steps) {
  stepper.moveRelativeInSteps(fw_steps);  
}

void Backward(long bw_steps) {
  stepper.moveRelativeInSteps(-bw_steps);  
}

void farbmessung() {

  ams.startMeasurement();

  bool rdy = false;
  while(!rdy) {
    delay(5);
    rdy = ams.dataReady();
  }
  

  
   
 unsigned long millis_now = millis();
 long timediff = millis_now - Starttime;
 if (timediff >= 30000) {
  timediff -= 30000;
  Starttime += 30000;
 }
 currentTime = (uint16_t)timediff;

 ams.readRawValues(values);
  values[0] = sensorValues[AS726x_VIOLET];
  values[1] = sensorValues[AS726x_BLUE];
  values[2] = sensorValues[AS726x_GREEN];
  values[3] = sensorValues[AS726x_YELLOW];
  values[4] = sensorValues[AS726x_ORANGE];
  values[5] = sensorValues[AS726x_RED];
}


void livefarbe() {
  farbmessung();
  if (sizeof(values) / sizeof(values[0]) > 0) {
    String violet = String(values[0]);
    String blue = String(values[1]);
    String green = String(values[2]);
    String yellow = String(values[3]);
    String orange = String(values[4]);
    String red = String(values[5]);
    Serial.println("f" + violet + "," + blue + "," + green + "," + yellow + "," + orange + "," + red);
  }
}



void send_in_utf_8(){
  
  Serial.print(currentTime); Serial.print(",");
  
  for (uint8_t i=0; i<AS726x_NUM_CHANNELS; i++) {
     Serial.print(values[i]); Serial.print(",");
  }
  
  Serial.println();  
}

long extract_motor_settings(String inp) {

  String s_p_s = "";

  String a_p_qs = "";
  
  String n_steps = "";


  uint8_t setting = 0;

/*example inp = [12+500+2] */

  for (int i = 1; i < inp.length(); i++) {

    if (isdigit(inp[i]) || inp[i] == '.') {
      if (setting == 0) {
        s_p_s += inp[i];
      }
      else if (setting == 1) {
        a_p_qs += inp[i];
      }
      else if (setting == 2) {
        n_steps += inp[i];
      }
    }
    
    else if (inp[i] == '+') {
      setting += 1;
    }
    
    else {
      break;
    }
  }

  stepper.setSpeedInStepsPerSecond(s_p_s.toDouble());
  stepper.setAccelerationInStepsPerSecondPerSecond(a_p_qs.toDouble());

  return n_steps.toInt();
  
}

/*
 *  Mocking Data and Test Function
 */

void testFunction() {
  Serial.println("Test message received!");
}






void Mocking_Data() {

 
 unsigned long millis_now = millis();
 long timediff = millis_now - Starttime;
 if (timediff >= 30000) {
  timediff -= 30000;
  Starttime += 30000;
 }
 currentTime = (uint16_t)timediff;
  

 // Generiere simulierten Lichtsensorwerte für jede Farbe (Kanal)
    double amplitudeRed = 1000.0; // Amplitude für den Rot-Kanal
    double frequencyRed = 0.1; // Frequenz für den Rot-Kanal
    double offsetRed = 500.0; // Versatz für den Rot-Kanal
    
    double amplitudeOrange = 800.0; // Amplitude für den Orange-Kanal
    double frequencyOrange = 0.15; // Frequenz für den Orange-Kanal
    double offsetOrange = 600.0; // Versatz für den Orange-Kanal
    
    double amplitudeYellow = 1200.0; // Amplitude für den Gelb-Kanal
    double frequencyYellow = 0.2; // Frequenz für den Gelb-Kanal
    double offsetYellow = 700.0; // Versatz für den Gelb-Kanal
    
    double amplitudeGreen = 600.0; // Amplitude für den Grün-Kanal
    double frequencyGreen = 0.25; // Frequenz für den Grün-Kanal
    double offsetGreen = 400.0; // Versatz für den Grün-Kanal
    
    double amplitudeBlue = 1000.0; // Amplitude für den Blau-Kanal
    double frequencyBlue = 0.3; // Frequenz für den Blau-Kanal
    double offsetBlue = 300.0; // Versatz für den Blau-Kanal
    
    double amplitudeViolet = 800.0; // Amplitude für den Violett-Kanal
    double frequencyViolet = 0.35; // Frequenz für den Violett-Kanal
    double offsetViolet = 200.0; // Versatz für den Violett-Kanal
    
    // Berechne die simulierten Werte für die sechs Kanäle des Lichtsensors
    for (int i = 0; i < AS726x_NUM_CHANNELS; i++) {
      double value;
      switch (i) {
        case 5:
          value = abs(amplitudeRed * sin(2 * PI * frequencyRed * currentTime / 1000.0) + offsetRed);
          break;
        case 4:
          value = abs(amplitudeOrange * sin(2 * PI * frequencyOrange * currentTime / 1000.0) + offsetOrange);
          break;
        case 3:
          value = abs(amplitudeYellow * sin(2 * PI * frequencyYellow * currentTime / 1000.0) + offsetYellow);
          break;
        case 2:
          value = abs(amplitudeGreen * sin(2 * PI * frequencyGreen * currentTime / 1000.0) + offsetGreen);
          break;
        case 1:
          value = abs(amplitudeBlue * sin(2 * PI * frequencyBlue * currentTime / 1000.0) + offsetBlue);
          break;
        case 0:
          value = abs(amplitudeViolet * sin(2 * PI * frequencyViolet * currentTime / 1000.0) + offsetViolet);
          break;
      }
      values[i] = (uint16_t)value;
    }
}
