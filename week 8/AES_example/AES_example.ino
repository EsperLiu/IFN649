#include <GCM.h>
#include <AES.h>
#include <Crypto.h>
#include "DHT.h"

#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11

#define LEDPIN 11

DHT dht(DHTPIN, DHTTYPE);

#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx

#define KEY_SIZE 16
#define IV_SIZE 12
#define AD_SIZE 8
#define CT_SIZE 32
#define PT_SIZE 32
#define TAG_SIZE 16

const int OUT_BUFFER_SIZE = IV_SIZE + AD_SIZE + CT_SIZE + TAG_SIZE; // this is 68

byte key[16] = {0};
byte iv[12] = {0};
uint8_t adata[8] = "HEADER"; 
byte ciphertext[32] = {0};
uint8_t plaintext[32] = {0};
byte tag[16] = {0};

byte out_buffer[OUT_BUFFER_SIZE] = {0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);

  // Setup DHT Sensor
  pinMode(DHTPIN, INPUT);
  dht.begin();

}

void loop() {
  // put your main code here, to run repeatedly:

  // Sensing temperature

  float t = dht.readTemperature();
  String s = "Temperature: " +  String(t);
  memcpy(plaintext, s.c_str(), 18);
  GCM<AES128> gcm;
  gcm.setKey(key, sizeof(key));

  for (int i=0; i < (int) sizeof(iv); i++){
    iv[i] = random(0,255);
  }

  gcm.setIV(iv, sizeof(iv));
  gcm.addAuthData(adata, sizeof(adata));
  gcm.encrypt(ciphertext, plaintext, sizeof(plaintext));
  gcm.computeTag(tag, sizeof(tag));

  memcpy(out_buffer, iv, sizeof(iv));
  memcpy(out_buffer + sizeof(iv), adata, sizeof(adata));
  memcpy(out_buffer + sizeof(iv) + sizeof(adata), ciphertext, sizeof(ciphertext));
  memcpy(out_buffer + sizeof(iv) + sizeof(adata) + sizeof(ciphertext), tag, sizeof(tag));
  
  Serial1.write(out_buffer, OUT_BUFFER_SIZE);

  for (int i = 0; i < OUT_BUFFER_SIZE; i++){
    Serial.printf("%X", out_buffer[i]);
    Serial.print(" ");
  }
  Serial.printf("\n%i bytes of data sent.\n", OUT_BUFFER_SIZE);

  delay(3000);
}
