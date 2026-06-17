String cmd = "";

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if (Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ON") {
      digitalWrite(LED_BUILTIN, HIGH);
    }

    else if (cmd == "OFF") {
      digitalWrite(LED_BUILTIN, LOW);
    }

    else if (cmd.startsWith("BLINK")) {

      int speed = cmd.substring(6).toInt();

      for(int i=0; i<80; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(speed);

        digitalWrite(LED_BUILTIN, LOW);
        delay(speed);
      }
    }
  }
}