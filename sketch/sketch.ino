//analog in A0 -->uscita anlogica del sensore
//digital in 2 -->usnita digitale del sensore
#include <stdio.h>
#include <Servo.h>
int gas_din=2;
int gas_ain=A0;
int ad_value;
int incomingByte = 0;
int valvola = 1; // 1 = aperta   |  0 = chiusa
char buffer[8];

Servo myservo;
int pos = 0;

volatile int stato = 0;
volatile int valv_stato = -1;

void scrivi_seriale(char tipo_messaggio, int value){
	sprintf(buffer,"%c%d%c",tipo_messaggio,value,'_');
	Serial.print(buffer);
	buffer[0]='\0';
}

void setup()
{
  myservo.attach(9);
	pinMode(gas_din,INPUT);
	pinMode(gas_ain,INPUT);
	Serial.begin(9600);
}
void loop()
{
 
	switch(stato){
		case 0:
			if(digitalRead(gas_din)==HIGH){//non c'è gas
				ad_value=analogRead(gas_ain);
				scrivi_seriale('w',ad_value);
			}
			if (digitalRead(gas_din)==LOW){//c'è gas
				ad_value=analogRead(gas_ain);
				scrivi_seriale('a',ad_value);
			} 
			if (Serial.available() > 0) {
				stato = 1;
				break;
			}
			delay(500);
			break;
		case 1:
			
			incomingByte = Serial.read();
			//applico la decisione dello stato in base al carattere ricevuto dal bot
			if(incomingByte == 'c') valv_stato = 0; //chiudi la valvola
			if(incomingByte == 'o') valv_stato = 1; //apri la valvola
			if(incomingByte == 'i') valv_stato = 2; //ignora emergenza
			//}
      		stato=0;
			break;
	}

	switch(valv_stato){
		case 0:
			//chiudo la vavola
			valvola = 0;
      for(pos = 0; pos < 90; pos += 1)
      {
        myservo.write(pos);
        delay(15);
      }
			break;
		case 1:
			//apro la valovla
			if(valvola != 1) valvola = 1;
      for(pos = 90; pos>=1; pos-=1)
      {
        myservo.write(pos);
        delay(15);
      }
			break;
		case 3:
			//ignoro l'emergenza
      		break;
	}
	valv_stato = -1;
  
	delay(500);
}
