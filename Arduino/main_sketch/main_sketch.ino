#include <Wire.h>
#include "Adafruit_AS726x.h"
#include <SpeedyStepper.h>

// Variablen zum Lesen der Port-Befehle
String command;
char firstchar;
double nullposition = 0;

// Arduino Outputs
const int LED_PIN = 13;
const int MOTOR_STEP_PIN = 3;
const int MOTOR_DIRECTION_PIN = 4;

// Titrationsphasen
boolean phase1 = false;
boolean phase2 = false;
boolean endphase = false;
boolean fertig = false;
boolean pause = false;

// Farbsensor Vergleichswerte 
int startvalues[6] = {0,0,0,0,0,0};
int values[6] = {0,0,0,0,0,0};


// Stellschrauben für den Ablauf
double change = 0.9; // gibt an bei wie viel Prozent der Ausgangsintensität eines Lichtwerts Phase 2 eingeleitet werden soll
double endvalue = 0.9; // gibt an bei wie viel Prozent der Ausgangsintensität eines Lichtwerts die Titration gestoppt wird
int endtime = 10000; // Wartezeit in ms zum überprüfen ob Titration fertig ist
double steps1 = 50; // gibt die Anzahl der Steps in Phase 1 an nach denen jeweils die Lichtwerte verglichen werden
double steps2 = 10; // gibt die Anzahl der Steps in Phase 2 an nach denen jeweils die Lichtwerte verglichen werden

// Objektinitialisierung zum ansteuern des Sensors und des Motors
SpeedyStepper stepper;
Adafruit_AS726x ams;
//buffer to hold Adafruit sensor raw values
uint16_t sensorValues[AS726x_NUM_CHANNELS];



void setup() {
  
  pinMode(LED_PIN, OUTPUT);   
  Serial.begin(9600); // connect to the serial port with 9600 as baudrate
  while(!Serial);

  if(!ams.begin()){ //begin and make sure we can talk to the sensor
    Serial.println("could not connect to sensor! Please check your wiring.");
    while(1);
  } // if Ende
  
  
  stepper.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN); // implement the wiring of the motor

  
} // setup Ende






void loop() {

  if (Serial.available() > 0) { //check if the serial port is available
    
    command = Serial.readString(); // read the incoming byte as String
    firstchar = command.charAt(0);
    
    check(firstchar); // die "check"-Funktion sucht nach befehlen und führt diese aus
    } // if Ende
    

  // Nachdem Befehle ausgeführt wurden wird mit der jeweiligen Phase fortgefahren

  // In Phase 1 werden zwischen den Lichtmessungen noch vergleichsweise viele Schritte ausgeführt, um die Zeit der Titration insgesamt zu verringern
  
  if (phase1){
    Serial.println("p1");
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
      Serial.println("p2");
      
    } // if Ende
  } // else if phase2 Ende

  // In der letzten Phase wird zu beginn eine gewisse Zeit gewartet, bevor erneut die Lichtwerte kontrolliert werden
  // Damit auf die Situation reagiert werden, dass der Indikator sich wieder entfärbt hat

  // Sollten  die Werte immernoch niedrig genug sein, wird die Titration gestoppt

  else if (endphase){
    Serial.println("p3");
    delay(endtime);
    farbmessung();
    livefarbe();
    for (int i=0;i<6;i++){
      if (values[i] < endvalue*startvalues[i]){
        endphase = false;
        Serial.println("p4");
         
      } // if Ende
      
      if (endphase){
        endphase = false;
        phase2 = true;
      } // if Ende
      
    } // for Ende
  } // else if Ende
  
} // loop Ende




/*
 *  Im Folgenden sind alle verwendeten Funktionen definiert
 */




void liveticker(double x){
  String steps = String(x);
  Serial.println("s"+steps);
}


void check(char firstchar){ // query of commands
  if (firstchar != ' '){ // first check if command is empty
      
      if (!phase1 && !phase2 && !endphase && firstchar == 'T'){ // command that titration starts
        farbmessung();
        startvalues[0] = sensorValues[AS726x_VIOLET];
        startvalues[1] = sensorValues[AS726x_BLUE];
        startvalues[2] = sensorValues[AS726x_GREEN];
        startvalues[3] = sensorValues[AS726x_YELLOW];
        startvalues[4] = sensorValues[AS726x_ORANGE];
        startvalues[5] = sensorValues[AS726x_RED];
      
        phase1 = true;
      } // if titration
      
      if (!phase1 && !phase2 && !endphase && firstchar == 'K'){ // command that calibration starts
        stepper.setSpeedInRevolutionsPerSecond(10.0);
        stepper.setAccelerationInRevolutionsPerSecondPerSecond(10.0);
        for (int i=0;i<15;i++){
          stepper.moveRelativeInSteps(500);
          nullposition += 500;
          delay(1000);
        } // for 
      } // if calibration
        
      if (firstchar == 'S'){ // stops titration
        phase1 = false;
        phase2 = false;
        endphase = false;
        pause = true;
        Serial.println("p5");
          
      } // if stop

      if (!phase1 && !phase2 && !endphase && firstchar == 'R'){
        stepper.setSpeedInRevolutionsPerSecond(10);
        stepper.setAccelerationInRevolutionsPerSecondPerSecond(10);
        stepper.moveRelativeInSteps(-nullposition);
      } // if Reset

      if (!phase1 && !phase2 && !endphase && firstchar == 'F'){
        stepper.setSpeedInRevolutionsPerSecond(10);
        stepper.setAccelerationInRevolutionsPerSecondPerSecond(10);
        stepper.moveRelativeInRevolutions(5);
      } // if vorwärts

      if (!phase1 && !phase2 && !endphase && firstchar == 'B'){
        stepper.setSpeedInRevolutionsPerSecond(10);
        stepper.setAccelerationInRevolutionsPerSecondPerSecond(10.0);
        stepper.moveRelativeInRevolutions(-5);
      } // if rückwärts

      if (!phase1 && !phase2 && !endphase && firstchar == 'N'){
        nullposition = 0;
      }

      if (!phase1 && !phase2 && !endphase && firstchar == 's'){
        if (change=0.9){
          change = 0.95;
          endvalue = 0.95;
        }
        else{
          change = 0.9;
          endvalue = 0.9;
        }
      }
      
  } // if
} // check

void moving(double x){
  stepper.setSpeedInRevolutionsPerSecond(10.0);
  stepper.setAccelerationInRevolutionsPerSecondPerSecond(10.0);
  stepper.moveRelativeInSteps(x);
  if (x > 0){
    liveticker(x);
  } // if Ende
  nullposition += x;
}

void farbmessung(){

  ams.startMeasurement(); //begin a measurement
  
  //wait till data is available
  bool rdy = false;
  while(!rdy){
    delay(5);
    rdy = ams.dataReady();
  } // while

  //read the values!
  ams.readRawValues(sensorValues);

  values[0] = sensorValues[AS726x_VIOLET];
  values[1] = sensorValues[AS726x_BLUE];
  values[2] = sensorValues[AS726x_GREEN];
  values[3] = sensorValues[AS726x_YELLOW];
  values[4] = sensorValues[AS726x_ORANGE];
  values[5] = sensorValues[AS726x_RED];


} // farbmessung

void livefarbe(){

  farbmessung();
  if (sizeof(values) > 0){
    String violet = String(values[0]);
    String blue = String(values[1]);
    String green = String(values[2]);
    String yellow = String(values[3]);
    String orange = String(values[4]);
    String red = String(values[5]);
    Serial.println("f"+violet+","+blue+","+green+","+yellow+","+orange+","+red);
  } // if
} // livefarbe
