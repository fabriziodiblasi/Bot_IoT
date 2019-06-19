//analog in A0 -->uscita anlogica del sensore
//digital in 2 -->usnita digitale del sensore
#include <stdio.h>
int gas_din=2;
int gas_ain=A0;
int ad_value;
int incomingByte = 0;
int valvola = 1; // 1 = aperta   |  0 = chiusa
char buffer[8];



volatile int stato = 0;
volatile int valv_stato = -1;
void setup()
{
	pinMode(gas_din,INPUT);
	pinMode(gas_ain,INPUT);
	Serial.begin(9600);
}
void loop()
{
 
	if(digitalRead(gas_din)==LOW) stato = 1; //c'è gas
	
	//if(digitalRead(gas_din)==HIGH && stato != 3 ) stato = 2; //non c'è gas. entro una sola volta nello stato di waiting
	if(digitalRead(gas_din)==HIGH) stato = 2;

	switch(stato){
		case 1:
			//rilevata fuga di gas
			ad_value=analogRead(gas_ain);
			sprintf(buffer,"%c%d%c",'a',ad_value,'_');
			/*
					Serial.print('a');
					Serial.print(ad_value);
			Serial.print('_');
			*/
			Serial.print(buffer);
			break;
		case 2:
			//nessuna fuga di gas
			/*
			ogni mezzo secondo invio la misurazione del gas a livello normale
			vecchia versione
			Serial.print("w");
			stato = 3; 
			break;
			*/
			while(true){
				ad_value=analogRead(gas_ain);
				sprintf(buffer,"%c%d%c",'w',ad_value,'_');
				Serial.print(buffer);
				
				if (digitalRead(gas_din)==HIGH){
					stato =1;
					break;
				} 

				if (Serial.available() > 0) {
					stato = 3;
					break;
				}
				delay(500);
			}
			break;
		case 3:
			/*lo stato 3 è quello che riceve dati dal bot python*/
			if (Serial.available() > 0) {
				// read the incoming byte:
				incomingByte = Serial.read();
				//applico la decisione dello stato in base al carattere ricevuto dal bot
				if(incomingByte == 'c') valv_stato = 0; //chiudi la valvola
				if(incomingByte == 'o') valv_stato = 1; //apri la valvola
				if(incomingByte == 'i') valv_stato = 2; //ignora emergenza
			}
			break;
	}

	switch(valv_stato){
		case 0:
			//chiudo la vavola
			valvola = 0;
			break;
		case 1:
			//apro la valovla
			if(valvola != 1) valvola = 1;
			break;
		case 3:
			//ignoro l'emergenza
      break;
	}

	delay(500);
}
