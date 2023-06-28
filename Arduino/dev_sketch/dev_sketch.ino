#include <Wire.h>
#include "Adafruit_AS726x.h"
#include "SpeedyStepper.h"

// Buffer to read the Serial port commands
String inputString = "";
bool stringComplete = false;
bool Start = false;


unsigned long Starttime = 0;
uint16_t currentTime;


bool mocking_data = false;


// Motor Outputs
const int MOTOR_STEP_PIN = 3;
const int MOTOR_DIRECTION_PIN = 4;

// Motor position buffer
double nullposition = 0;


// Phases of titration
/*
 * 0 ~ break
 * 1 ~ first phase
 * 2 ~ second phase
 * 3 ~ last phase
 * 4 ~ finish
 */
uint8_t ph = 0;

// Light sensor buffer
uint16_t startvalues[AS726x_NUM_CHANNELS];
uint16_t values[AS726x_NUM_CHANNELS];


// Adjustments for the process
double change = 0.9; // indicates at what percentage of the initial intensity of a light value phase 2 should be initiated
double endvalue = 0.9; // indicates at what percentage of the initial intensity of a light value the titration should stop
uint16_t endtime = 10000; // waiting time in ms to check if titration is finished
double steps1 = 50; // indicates the number of steps in phase 1 after which the light values are compared
double steps2 = 10; // indicates the number of steps in phase 2 after which the light values are compared

// Object initialization to control the sensor and the motor
SpeedyStepper stepper;
Adafruit_AS726x ams;

void setup(void) {

  Serial.begin(9600);
  while(!Serial);

  pinMode(LED_BUILTIN, OUTPUT);

  if (!ams.begin()) {
    Serial.println("could not connect to sensor! Please check your wiring.");
    while(1);
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

    if (inputString == "Start\n" && ph == 0) {
      Start = true;
      
    }

    else if (inputString == "mock\n" && !mocking_data) {
      mocking_data = true;
      Starttime = millis();
    }

    else if (inputString == "Stop\n") {
      Start = false;
      ph = 0;
      mocking_data = false;
    }

    else if (inputString == "Kalibriere\n") {
      Calibration();
    }

    else if (inputString == "Reset\n") {
      Reset();
    }

    else if (inputString == "Forward\n") {
      Forward();
    }

    else if (inputString == "Backward\n") {
      Backward();
    }

    else if (inputString == "Nullposition\n") {
      nullposition = 0;
    }

    else if (inputString.startsWith("double")) {

      String digit_chars = "";
      
      for (uint8_t cha = 6; cha < inputString.length(); cha++) {

        if (!isdigit(inputString[cha])) {
          break;
        }
        digit_chars += inputString[cha];        
      }
      int response_int = digit_chars.toInt() * 2;
      Serial.println(response_int);
    }
    inputString = "";
    stringComplete = false;
  }

  if (Start == true) {
    measurement();
    send_in_utf_8();
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

void Calibration() {
  
}

void Reset() {
  
}

void Forward() {
  stepper.setSpeedInRevolutionsPerSecond(3);
  stepper.setAccelerationInRevolutionsPerSecondPerSecond(3.0);
  stepper.moveRelativeInRevolutions(25);  
}

void Backward() {
  stepper.setSpeedInRevolutionsPerSecond(3);
  stepper.setAccelerationInRevolutionsPerSecondPerSecond(3.0);
  stepper.moveRelativeInRevolutions(-25);  
}

void measurement() {

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

void send_in_utf_8(){
  
  Serial.print(currentTime); Serial.print(",");
  
  for (uint8_t i=0; i<AS726x_NUM_CHANNELS; i++) {
     Serial.print(values[i]); Serial.print(",");
  }
  
  Serial.println();  
}
