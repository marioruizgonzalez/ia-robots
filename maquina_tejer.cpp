#define DIR_PIN 8
#define STEP_PIN 9
#define BUTTON_UP 10  // Botón para aumentar pasos
#define BUTTON_DOWN 11  // Botón para disminuir pasos

int steps = 200;  // Número inicial de pasos

void setup() {
  Serial.begin(9600);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(BUTTON_UP, INPUT_PULLUP);
  pinMode(BUTTON_DOWN, INPUT_PULLUP);
}

void loop() {
  // Leer el estado de los botones
  if (digitalRead(BUTTON_UP) == LOW) {
    steps += 50;  // Aumentar pasos
    delay(200);  // Debounce
  }
  if (digitalRead(BUTTON_DOWN) == LOW) {
    steps -= 50;  // Disminuir pasos
    delay(200);  // Debounce
  }

  // Limitar el número de pasos a un rango razonable
  steps = constrain(steps, 50, 1000);

  // Establecer la dirección del motor (CW o CCW)
  digitalWrite(DIR_PIN, HIGH); // Cambia a LOW para cambiar la dirección

  // Girar el motor en un sentido
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(2000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(2000);
  }

  delay(1000); // Esperar un segundo

  // Cambiar la dirección del motor (CW o CCW)
  digitalWrite(DIR_PIN, LOW); // Cambia a HIGH para cambiar la dirección

  // Girar el motor en el otro sentido
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(2000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(2000);
  }

  delay(1000); // Esperar un segundo
}
