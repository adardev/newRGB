#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pines de sensores
const int pinHumAmb = A0;
const int pinHumTierra = A1;
const int pinTemp = A2;

// Pines de salida
const int Foco = 7;
const int Ventilador1 = 5;
const int Ventilador2 = 6;
const int Bomba = 8;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);

  // Configurar pines como salida
  pinMode(Foco, OUTPUT);
  pinMode(Ventilador1, OUTPUT);
  pinMode(Ventilador2, OUTPUT);
  pinMode(Bomba, OUTPUT);
}

void loop() {
  // Leer sensores analógicos
  int valorTemp = analogRead(pinTemp);
  int valorHumAmb = analogRead(pinHumAmb);
  int valorHumTierra = analogRead(pinHumTierra);

  // Convertir lecturas (ejemplo simple, puedes ajustar fórmulas)
  //float tempC = (valorTemp * 5.0 / 1023.0) * 100;  // simplificada
  //int humAmb = map(valorHumAmb, 0, 1023, 0, 100);
  //int humTierra = map(valorHumTierra, 0, 1023, 0, 100);
  
  float tempC = 1.0;
  int humAmb = 2.0;
  int humTierra = 3.0;

  // Leer estados digitales
  int focoEstado = digitalRead(Foco);
  int ventiladorEstado = digitalRead(Ventilador1); // o puedes combinar ambos
  int bombaEstado = digitalRead(Bomba);

  // Imprimir una línea bien formateada
  Serial.print("temp=");
  Serial.print(tempC, 1);  // 1 decimal
  Serial.print("&hum_amb=");
  Serial.print(humAmb);
  Serial.print("&hum_tierra=");
  Serial.print(humTierra);
  Serial.print("&foco=");
  Serial.print(focoEstado);
  Serial.print("&ventilador=");
  Serial.print(ventiladorEstado);
  Serial.print("&bomba=");
  Serial.println(bombaEstado);  // <- println para marcar fin de línea

  delay(3000);  // Espera antes de la siguiente lectura
}
