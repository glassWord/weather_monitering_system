#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// Pin definitions
#define DHTPIN 2       // Pin connected to the DHT11 sensor
#define DHTTYPE DHT11  // DHT 11
#define RAINPIN 3      // Pin connected to the rain sensor
#define MQ135PIN A0    // Pin connected to the MQ-135 sensor
#define buzzer 4

// Initialize the DHT sensor
DHT dht(DHTPIN, DHTTYPE);

// Initialize the LCD with I2C address 0x27 (you may need to change this address for your LCD)
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Start serial communication
  Serial.begin(9600);
  
  // Start DHT sensor
  dht.begin();
  
  // Set the rain sensor and MQ-135 sensor pins as input
  pinMode(RAINPIN, INPUT);
  pinMode(MQ135PIN, INPUT);
  pinMode(buzzer,OUTPUT);
  
  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.print("Weather Station");
  delay(2000); // Wait for 2 seconds
  lcd.clear();
}

void loop() {
  // Reading temperature and humidity from DHT11
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error!");
    return;
  }

  // Reading rain sensor
  int rainValue = digitalRead(RAINPIN);
//  String rainStatus = (rainValue == LOW) ? "Rain" : "No Rain";
if(rainValue ==LOW)
{
  digitalWrite(buzzer,HIGH);
}
else
{
  digitalWrite(buzzer,LOW);
}
  

  // Reading MQ-135 sensor (Air Quality)
  int airQuality = analogRead(MQ135PIN);

  // Printing the results to the serial monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C");
  
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Rain status: ");
  Serial.println(rainValue );

  Serial.print("Air Quality (MQ-135): ");
  Serial.println(airQuality);

  // Displaying the results on the LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C");
  
  lcd.setCursor(0, 1);
  lcd.print("Hum: ");
  lcd.print(humidity);
  lcd.print(" %");
  
  delay(2000); // Display for 2 seconds

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Rain: ");
  lcd.print(rainValue );
  
  lcd.setCursor(0, 1);
  lcd.print("AirQ: ");
  lcd.print(airQuality);
  
  // Wait a few seconds between measurements.
  delay(2000);
}