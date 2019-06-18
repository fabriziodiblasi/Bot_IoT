//analog in A0 -->uscita anlogica del sensore
//digital in 2 -->usnita digitale del sensore
#include <stdio.h>
int gas_din=2;
int gas_ain=A0;
int ad_value;

char buffer[8];


void setup()
{
  pinMode(gas_din,INPUT);
  pinMode(gas_ain,INPUT);
  Serial.begin(9600);
}

void loop()
{
  
  if(digitalRead(gas_din)==LOW){ //c'è gas
    ad_value=analogRead(gas_ain);
    sprintf(buffer,"%c%d%c",'H',ad_value,'_');
    Serial.print(buffer);
  }
  
  if(digitalRead(gas_din)==HIGH){//no gas
    ad_value=analogRead(gas_ain);
    sprintf(buffer,"%c%d%c",'L',ad_value,'_');
    Serial.print(buffer);
  }
  delay(500);
}
