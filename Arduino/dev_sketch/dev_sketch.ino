#include <Wire.h>
#include "Adafruit_AS726x.h"
#include "SpeedyStepper.h"

// Buffer to read the Serialport commands
String inputString = "";
bool stringComplete = false;
bool Start = false;


// Motor Outputs
const int MOTOR_STEP_PIN = 3;
const int MOTOR_DIRECTION_PIN = 4;

// Motorposition buffer
double nullposition = 0;


// Titrationsphasen
/*
 * 0 ~ Pause
 * 1 ~ Erste Phase
 * 2 ~ Zweite Phase
 * 3 ~ Endphase
 * 4 ~ Fertig
 */
uint8_t ph = 0;

// Farbsensor buffer
uint16_t startvalues[6];
uint16_t values[6];


// Stellschrauben für den Ablauf
double change = 0.9; // gibt an bei wie viel Prozent der Ausgangsintensität eines Lichtwerts Phase 2 eingeleitet werden soll
double endvalue = 0.9; // gibt an bei wie viel Prozent der Ausgangsintensität eines Lichtwerts die Titration gestoppt wird
uint16_t endtime = 10000; // Wartezeit in ms zum überprüfen ob Titration fertig ist
double steps1 = 50; // gibt die Anzahl der Steps in Phase 1 an nach denen jeweils die Lichtwerte verglichen werden
double steps2 = 10; // gibt die Anzahl der Steps in Phase 2 an nach denen jeweils die Lichtwerte verglichen werden

// Objektinitialisierung zum ansteuern des Sensors und des Motors
SpeedyStepper stepper;
Adafruit_AS726x ams;

void setup(void) {

  Serial.begin(9600);
  while(!Serial);

  Serial.println("Setup-Ready");

  /*if (!ams.begin()) {
    Serial.println("could not connect to sensor! Please check your wiring.");
    while(1);
  }

  stepper.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN); // implement the wiring of the motor  */
}



void loop(void) {

  if (stringComplete) {
    Serial.println(inputString);

    /*
     * Ab Hier werden je nach Inhalt des Seriellen Ports Befehle ausgeführt.
     */

    if (inputString == "Start\n" && ph == 0) {
      Start = true;
    }

    else if (inputString == "Stopp\n") {
      Start = false;
      ph = 0;
    }

    else if (inputString == "Kalibriere\n") {
      Calibration();
    }

    else if (inputString == "Reset\n") {
      Reset();
    }

    else if (inputString == "Forward\n") {
      Move();
    }

    else if (inputString == "Backward\n") {
      Move();
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
    }
  }
}

void Calibration() {
  
}

void Reset() {
  
}

void Move() {
  
}
