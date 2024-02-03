#define MOSFET 8

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  pinMode(MOSFET, OUTPUT);
  digitalWrite(MOSFET, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  digitalWrite(MOSFET, HIGH);
  delay(1000);
  digitalWrite(MOSFET, LOW);
  delay(1000);
}
