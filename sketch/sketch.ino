//analog in A0 -->uscita anlogica del sensore
//digital in 2 -->usnita digitale del sensore
//pin 6 sensore di flusso
//pin 7 sensore di chiusura
#include <stdio.h>
#include <Servo.h>
int flow_sensor = 4;
int close_sensor = 7;
int gas_din = 2;
int gas_ain = A0;
int ad_value;
int incomingByte = 0;
int valvola = 1; // 1 = aperta   |  0 = chiusa
char buffer[8];

Servo myservo;
int pos = 0;

volatile int stato = 0;
volatile int valv_stato = 1;

void scrivi_seriale(char tipo_messaggio, int value){
	sprintf(buffer,"%c%d%c",tipo_messaggio,value,'_');
	Serial.print(buffer);
	buffer[0]='\0';
}

void apri_valvola(){
	for(pos = 180; pos>=1; pos-=1){
		myservo.write(pos);
		delay(15);
	}
}

void chiudi_valvola(){
	for(pos = 0; pos < 170; pos += 1){
		myservo.write(pos);
		delay(15);
	}
}


void setup()
{
  	myservo.attach(9);
  	pinMode(gas_din,INPUT);
  	pinMode(gas_ain,INPUT);
    pinMode(flow_sensor,INPUT);
    pinMode(close_sensor,INPUT);
  	Serial.begin(9600);
  	apri_valvola();
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

	//valvola : 1 = aperta   |  0 = chiusa
	switch(valv_stato){
		case 0:
			//chiudo la vavola
			if(valvola == 1){
				valvola = 0;
				
				chiudi_valvola();
        delay(1000);
				
				// gli switch sono normalmente aperti.
				// se premo lo switch il circuito si chiude e passa corrente
				
				if(digitalRead(close_sensor) == LOW || digitalRead(flow_sensor) == HIGH){
				//if(digitalRead(close_sensor) == LOW ){	
					/*
					se premo lo switch del sensore di flusso significa che pur essendo chiuso 
					ho un passaggio di gas
					*/
					if(digitalRead(close_sensor) == LOW) scrivi_seriale('e',0);
					if(digitalRead(flow_sensor) == HIGH) scrivi_seriale('f',0);// f = flow
					// "f0_" = errore per il controllo del flusso
				}else{
					scrivi_seriale('T',0);//True
				}
				
			}
			break;
		case 1:
			//apro la valovla
			if(valvola == 0){

			 	valvola = 1;
				apri_valvola();
				
				delay(1000);
       
				if(digitalRead(close_sensor) == HIGH || digitalRead(flow_sensor) == LOW){
				//if(digitalRead(close_sensor) == HIGH){
					/*
					se premo lo switch del sensore di flusso significa che pur essendo chiuso 
					ho un passaggio di gas
					*/
					if(digitalRead(close_sensor) == HIGH) scrivi_seriale('e',1);
          if(digitalRead(flow_sensor) == LOW) scrivi_seriale('f',1);// f = flow
					// "f0_" = errore per il controllo del flusso
				}else{
					scrivi_seriale('T',1);//True
				}
							
			}
			break;
		case 3:
			//ignoro l'emergenza
	  		break;
	}
	//valv_stato = -1;
  
	delay(500);
}
