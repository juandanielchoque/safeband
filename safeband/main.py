from machine import Pin
import time
import random
import network
from umqtt.simple import MQTTClient 

# Configuración Wi-Fi
SSID = 'WifiTapara-2.4G'
PASSWORD = '12345678'

# Configuración del servidor MQTT
mqtt_server = '161.132.38.212'  # Dirección IP del servidor MQTT
mqtt_port = 1883  # Puerto del servidor MQTT
mqtt_topic = b'datos'  # Tema de MQTT donde se publicarán los datos

# Configurar la conexión Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    pass

print('Conectado a WiFi')

# Función para conectar al servidor MQTT y publicar datos
def conectar_y_enviar():
    client = MQTTClient('ESP32_Cliente', mqtt_server, port=mqtt_port)
    try:
        client.connect()
        print('Conectado a servidor MQTT')
    except OSError as e:
        print('Error de conexión MQTT:', e)
        return
    
    inclination_sensor = Pin(15, Pin.IN, Pin.PULL_UP)

    while True:
        state = inclination_sensor.value()
        if state == 0:
            # Sensor inclinado / simular persona en problemas / 100 - 125
            data = random.randint(110, 125)
        else:
            # Sensor no inclinado / simular persona en estado normal / 60 - 70
            data = random.randint(65, 70)
        
        print('Enviando dato MQTT:', data)
        
        try:
            # Publicar el dato en el tema MQTT configurado
            client.publish(mqtt_topic, bytes(str(data), 'utf-8'))
            print('Dato enviado correctamente')
        except OSError as e:
            print('Error al publicar MQTT:', e)
        
        time.sleep(2.5)

# Llamar a la función principal para conectar y enviar datos
conectar_y_enviar()
