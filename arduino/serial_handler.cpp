#include "serial_handler.h"
#include <Arduino.h>

void SerialHandler::sendMsg(String msg) {
  Serial.println("Arduino: " + msg);
}
