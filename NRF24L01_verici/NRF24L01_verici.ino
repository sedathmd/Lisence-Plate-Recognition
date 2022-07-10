#include  <SPI.h> 
#include "nRF24L01.h"
#include "RF24.h"    

int datafromUser=0;
int led=2;
 
int mesaj[1];  
    
RF24 verici(9,10);

const int kanal = 111; 
  

void setup()
{
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  verici.begin(); 
  verici.openWritingPipe(kanal);
}


void loop()
{
  if(Serial.available() > 0)
  {
    datafromUser=Serial.read();
  }
  if(datafromUser == '1')
  {
    digitalWrite(led, HIGH);
    mesaj[0] = 50; 
    verici.write(&mesaj, sizeof(mesaj));
  }
  
  if(datafromUser == '0')
  { 
    digitalWrite(led, LOW);
  }  
}
