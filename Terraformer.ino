#include <Adafruit_BMP280.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

Adafruit_BMP280 bmp;
float sensorVoltage;
float valor;
int indice_uv = 0;

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

void setup() {
  Serial.begin(9600);
  ss.begin(GPSBaud);
  pinMode(A1, OUTPUT);

  unsigned status;
  status = bmp.begin();
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                      "try a different address!"));
    while (1) delay(10);
  }

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16, Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_500);
}

void loop() {
  while (ss.available() > 0) {
    if (gps.encode(ss.read())) {
      Serial.print(F("LONGITUD = "));
      Serial.print(gps.location.lng(), 6);
      Serial.print(F(" LATITUD = "));
      Serial.print(gps.location.lat(), 6);
      
       valor = analogRead(A1);
  sensorVoltage = valor / 1024 * 5.0;
  Serial.print(" Lectura sensor UV = ");
  Serial.print(valor);
  Serial.print(" Voltaje sensor UV = ");
  Serial.print(sensorVoltage);
  Serial.print(" V");

  valor = analogRead(A1);
  if (valor<227)
    indice_uv = 0;
  else if (valor>=227 && valor<318)
    indice_uv=1;
  else if (valor>=318 && valor<408)
    indice_uv=2;
  else if (valor>=408 && valor<503)
    indice_uv=3;
  else if (valor>=503 && valor<606)
    indice_uv=4;
  else if (valor>=606 && valor<696)
    indice_uv=5;
  else if (valor>=696 && valor<795)
    indice_uv=6;
  else if (valor>=795 && valor<881)
    indice_uv=7;
  else if (valor>=881 && valor<976)
    indice_uv=8;
  else if (valor>=976 && valor<1079)
    indice_uv=9;
  else if (valor>=1079 && valor<1170)
    indice_uv=10;
  else if (valor>1170)
    indice_uv = 11;
     
  Serial.print(" Indice UV = ");
  Serial.print(indice_uv);

  Serial.print(F(" Temperature: "));
  Serial.print(bmp.readTemperature());
  

  Serial.print(F(" Pressure: "));
  Serial.print(bmp.readPressure());
  Serial.print(F(" Altitude: "));
  Serial.print(bmp.readAltitude(1013.25));
  Serial.println(" m ");
    }
  }

  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("No GPS detected: check wiring."));
    while (true);
  }

 }

