#include <WiFi.h>
#include <PubSubClient.h>

int servoPin = 14;
int sensor = 15;
int check = 0;
int count = 0;


// Replace the next variables with your SSID/Password combination
const char* ssid = "Tien";
const char* password = "12345679";

const char* mqtt_server = "192.168.137.1";
WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
  Serial.begin(115200);
  pinMode(sensor, INPUT);
  pinMode(servoPin, OUTPUT);
  digitalWrite(servoPin, LOW);
  
  setup_wifi();
  client.setServer(mqtt_server, 8900);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  Serial.println(message[0]);
  if (message[0] == '1'){
    Serial.println("a");
    digitalWrite(servoPin, HIGH);
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("resultPlate");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  
  int check = digitalRead(sensor);// doc tin hieu dien tu chan digital sensor
  if (check == 0 && count == 0){       
    count = 1;    
  }
  if(check == 1 && count == 1){
  count = 0;
  delay(2000);
  Serial.println("bb");
  digitalWrite(servoPin, LOW);
  }
}
