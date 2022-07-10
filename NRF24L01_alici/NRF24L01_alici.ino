#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"   
#include <Servo.h>

Servo servoM;
int mesaj[1];

RF24 alici(9,10);

const int kanal = 111;


void setup(){
  servoM.attach(2);
  servoM.write(0);
  alici.begin();
  alici.openReadingPipe(1,kanal);
  alici.startListening();
}

void loop(){
  if (alici.available())
  {
    bool done = false;    
    while (!done){
      
      done = alici.read(&mesaj, sizeof(mesaj));      
      if (mesaj[0] == 50){
        delay(10);
        servoM.write(90);
        
      }
      else {
        
        servoM.write(0);
      }
      delay(10);
    }
  }
}
