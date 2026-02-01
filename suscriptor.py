import ssl
import paho.mqtt.client as mqtt
import psycopg2

# Configuración MQTT
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
USERNAME = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASS")
TOPIC_INT = "sensores/enteros"
TOPIC_FLOAT = "sensores/flotantes"

# Configuración Base de Datos
DB_PARAMS = {
    "host": "localhost",
    "database": "postgres",
    "user": "karen",
    "password": ""
}

def save_to_db(topic, payload):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        if topic == TOPIC_INT:
            val = int(payload)
            query = "INSERT INTO lake_raw_data_int (topic, payload, value) VALUES (%s, %s, %s)"
        else:
            val = float(payload)
            query = "INSERT INTO lake_raw_data_float (topic, payload, value) VALUES (%s, %s, %s)"
            
        cur.execute(query, (topic, payload, val))
        conn.commit()
        cur.close()
        conn.close()
        print("Dato guardado en base de datos")
    except Exception as e:
        print("Error en base de datos:", e)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al Broker")
        client.subscribe([(TOPIC_INT, 0), (TOPIC_FLOAT, 0)])
    else:
        print("Error de conexion:", rc)

def on_message(client, userdata, msg):
    payload_decoded = msg.payload.decode(errors='ignore')
    print("Mensaje recibido:", msg.topic, payload_decoded)
    save_to_db(msg.topic, payload_decoded)

# Inicializacion
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

print("Iniciando suscriptor...")
client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()