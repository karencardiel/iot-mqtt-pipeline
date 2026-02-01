import ssl
import paho.mqtt.client as mqtt
import random
import time

# --- MISMAS CREDENCIALES QUE EL SUSCRIPTOR ---
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
USERNAME = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASS")
# Topicos
TOPIC_INT = "sensores/enteros"
TOPIC_FLOAT = "sensores/flotantes"

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

print("Conectando al broker para enviar datos...")
client.connect(BROKER, PORT)

try:
    while True:
        # 1. Generar y publicar entero
        val_int = random.randint(0, 100)
        client.publish(TOPIC_INT, val_int)
        print(f"Enviado Entero: {val_int} a {TOPIC_INT}")

        # 2. Generar y publicar flotante 
        val_float = round(random.uniform(0.0, 100.0), 2)
        client.publish(TOPIC_FLOAT, val_float)
        print(f"Enviado Flotante: {val_float} a {TOPIC_FLOAT}")

        time.sleep(5) # Envía datos cada 5 segundos
except KeyboardInterrupt:
    print("Publicador detenido.")
    client.disconnect()