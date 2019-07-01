int flow_sensor = 4;
int close_sensor = 7;

void setup() {
  // put your setup code here, to run once:
  pinMode(flow_sensor,INPUT);
  pinMode(close_sensor,INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if(digitalRead(flow_sensor)==HIGH){
    Serial.println("flow_sensor : HIGH");
  }
  
  if(digitalRead(flow_sensor)==LOW){
    Serial.println("flow_sensor : LOW");
  }
  delay(500);
  
  /*
  if(digitalRead(close_sensor)==HIGH){
    Serial.println("close_sensor : HIGH");
  }
   if(digitalRead(close_sensor)==LOW){
    Serial.println("close_sensor : LOW");
  }
  */
  delay(500);
}
