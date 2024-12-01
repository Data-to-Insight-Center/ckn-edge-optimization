import base64
import random
import paho.mqtt.client as mqtt
import json
import time

from confluent_kafka import Producer
from utils import predict, pre_process, model_store, process_qoe, delivery_report

broker = '149.165.174.52'
port = 1883
topic = "camera-trap/predict"
client_id = f'subscriber-{random.randint(0, 100)}'

producer = Producer({'bootstrap.servers': '149.165.170.250:9092'})


def connect_mqtt():
    """Connect to the MQTT broker and acknowledge successful connection."""
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker successfully!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt.Client(client_id)
    client.on_connect = on_connect

    try:
        client.connect(broker, port, 60)
    except Exception as e:
        print(f"Error connecting to MQTT Broker: {e}")
        exit(1)

    return client


def handle_message(payload):
    """Handle the incoming message and process the file."""
    try:
        # Parse the JSON payload
        data = json.loads(payload)

        # Extract file data and save it
        file_data = base64.b64decode(data.pop("file"))
        file_path = "image.jpg"
        with open(file_path, "wb") as file:
            file.write(file_data)

        image_save_time = time.perf_counter()

        preprocessed_input = pre_process("image.jpg")
        image_preprocessed_time = time.perf_counter()

        prediction, probability = predict(preprocessed_input)
        image_predicted_time = time.perf_counter()

        qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_time - image_save_time, float(data['delay']),
                                              float(data['accuracy']))
        current_model_id = model_store.get_current_model_id()
        qoe_computed_time = time.perf_counter()

        kafka_payload = json.dumps({'model_id': current_model_id, 'qoe': qoe, 'accuracy_qoe': acc_qoe,
                                    'delay_qoe': delay_qoe, 'prediction': prediction, 'probability': probability})
        producer.produce('ckn-event', kafka_payload, callback=delivery_report)
        producer.flush(timeout=1)
        event_produced_time = time.perf_counter()

    except Exception as e:
        print(f"Error handling message: {e}")


def subscribe(client):
    """Subscribe to the MQTT topic and process messages."""
    def on_message(client, userdata, msg):
        print(f"Received message from topic `{msg.topic}`")
        handle_message(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def run():
    """Run the MQTT subscriber."""
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
