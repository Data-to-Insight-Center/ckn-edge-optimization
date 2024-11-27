import json
import time
import base64
import io
from PIL import Image
import paho.mqtt.client as mqtt
from confluent_kafka import Producer
from utils import predict, pre_process, model_store, save_file, process_qoe, delivery_report

# MQTT setup
MQTT_BROKER = 'localhost' # '149.165.174.52'
MQTT_PORT = 1883
INPUT_TOPIC = 'prediction/input'
OUTPUT_TOPIC = 'prediction/output'
mqtt_client = mqtt.Client()

producer = Producer({'bootstrap.servers': '149.165.170.250:9092'})

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(INPUT_TOPIC)  # Subscribe to the prediction input topic


# Callback when a message is received
def on_message(client, userdata, msg):
    server_receive_time = time.perf_counter()
    print(f"Received message: {msg.payload}")

    # Parse the JSON payload
    request_data = json.loads(msg.payload)

    # Decode the base64 image data
    image_data_base64 = request_data['image_data']
    image_data = base64.b64decode(image_data_base64)  # Decoding the base64 string
    file_data = Image.open(io.BytesIO(image_data))  # Open image from the decoded bytes

    filename = save_file(file_data)
    image_save_time = time.perf_counter()

    preprocessed_input = pre_process(filename)
    image_preprocessed_time = time.perf_counter()

    prediction, probability = predict(preprocessed_input)
    image_predicted_time = time.perf_counter()

    qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_time - image_save_time, float(request_data['delay']), float(request_data['accuracy']))
    current_model_id = model_store.get_current_model_id()
    qoe_computed_time = time.perf_counter()

    kafka_payload = json.dumps({'model_id': current_model_id, 'qoe': qoe, 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe})
    producer.produce('ckn-event', kafka_payload, callback=delivery_report)
    producer.flush(timeout=1)
    event_produced_time = time.perf_counter()

    response_json = json.dumps({
        "server_receive_time": server_receive_time,
        "image_save_time": image_save_time,
        "image_preprocessed_time": image_preprocessed_time,
        "image_predicted_time": image_predicted_time,
        "qoe_computed_time": qoe_computed_time,
        "event_produced_time": event_produced_time,
        "response_create_time": time.perf_counter()
    })

    client.publish(OUTPUT_TOPIC, response_json)


# Set up callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop to listen for messages
mqtt_client.loop_forever()
