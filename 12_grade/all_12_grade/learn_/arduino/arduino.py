import serial
import time

# Define the serial port and baud rate
serial_port = 'COM3'  # Change this to the appropriate port
baud_rate = 9600

# Connect to the Arduino board
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # Wait for a message from Arduino
        response = ser.readline().decode('utf-8').strip()
        if response:
            print("Message from Arduino:", response)
            # if int(response) == 100100:
            #     response = 10000
            print("dofek", int(response) // 55.5 + 40)
finally:
    ser.close()  # Close the serial port when done


# int potPin = A0; // potentiometer is connected to analog 0 pin
# int led1 = 12; // red LED connected to digital PIN 13
# int led2 = 10; // red LED connected to digital PIN 12
# int led3 = 8;
# int potValue; // variable used to store the value coming from the sensor
# int percent; // variable used to store the percentage value
#
# void setup() {
# pinMode(led1, OUTPUT); // LED is declared as an output
# pinMode(led2, OUTPUT);
# pinMode(led3, OUTPUT);
# Serial.begin(9600);
# }
#
# void loop() {
# potValue = analogRead(potPin); // read the value from the potentiometer and assign the name potValue
# percent = map(potValue, 0, 1023, 0, 100); // convert potentiometer reading to a percentage
# Serial.print(percent);
# Serial.println(percent);
# if (percent <= 5) { //if the percentage is less than 5%...
#     digitalWrite(led1, LOW);
#     digitalWrite(led2, LOW);
#     digitalWrite(led3, LOW);
# }
# else if(percent > 5 && percent <= 40){
#     digitalWrite(led1, HIGH);
#     digitalWrite(led2, LOW);
#     digitalWrite(led3, LOW);
#
# }
# else if(percent > 40 && percent <= 70){
#     digitalWrite(led1, HIGH);
#     digitalWrite(led2, HIGH);
#     digitalWrite(led3, LOW);
# }
# else{
#     digitalWrite(led1, HIGH);
#     digitalWrite(led2, HIGH);
#     digitalWrite(led3, HIGH);
# }
# }
