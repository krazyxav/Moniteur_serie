#include<Wire.h>
const int MPU=0x68; 
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
char userInput;

void  setup(){
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);  
  Wire.write(0);    
  Wire.endTransmission(true);
  Serial.begin(9600);
}
void  loop(){
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,12,true);  
  AcX=Wire.read()<<8|Wire.read();    
  AcY=Wire.read()<<8|Wire.read();
  AcZ=Wire.read()<<8|Wire.read();  
  GyX=Wire.read()<<8|Wire.read();  
  GyY=Wire.read()<<8|Wire.read();  
  GyZ=Wire.read()<<8|Wire.read();  


  /*
  Serial.print("AcX=");Serial.println(AcX);
  Serial.print("AcY=");Serial.println(AcY);
  Serial.print("AcZ=");Serial.println(AcZ);
  
  Serial.print("GyX=");Serial.println(GyX);
  Serial.print("GyY=");Serial.println(GyY);
  Serial.print("GyZ=");Serial.println(GyZ);
  */
  if(Serial.available()>0){
    userInput=Serial.read();
    if(userInput == 'a'){
      Serial.print(AcX);Serial.print("|");Serial.print(AcY);Serial.print("|");Serial.print(AcZ);Serial.print("|");
      Serial.print(GyX);Serial.print("|");Serial.print(GyY);Serial.print("|");Serial.println(GyZ);
    } 
  }

  //Serial.println(" ");
}
