import paho.mqtt.client as mqtt
import json
import base64
import csv
import time

# MQTT setup
MQTT_BROKER = 'localhost'  # Adjust this to your broker IP
MQTT_PORT = 1883
INPUT_TOPIC = 'prediction/input'
OUTPUT_TOPIC = 'prediction/output'
mqtt_client = mqtt.Client()

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, rc):
    for i in range(1000):
        file_location = "abacus.jpg"
        with open(file_location, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        payload = {
            "accuracy": "0.849",
            "delay": "0.051",
            "server_id": "EDGE-1",
            "service_id": "imagenet_image_classification",
            "client_id": f"raspi-1-{i}",
            "added_time": "03-04-2023 15:13:05",
            "ground_truth": "abacus",
            "image_data": image_data
        }

        # Capture client send time just before publishing the message
        client_send_time = time.perf_counter()

        # Store the send time in userdata so it can be accessed in on_message
        userdata = {'client_send_time': client_send_time}

        # Send the request with the userdata (which contains client_send_time)
        client.publish(INPUT_TOPIC, json.dumps(payload), qos=0, retain=False, userdata=userdata)
        print(f"Request {i + 1} sent at time {client_send_time}.")

        # Wait for a response (blocking until response is received)
        client.loop_start()  # Start the MQTT loop to process messages


# Callback when a result message is received
def on_message(client, userdata, msg):
    result_data = json.loads(msg.payload)
    client_receive_time = time.perf_counter()  # Record client receive time

    # Retrieve the client_send_time from userdata
    client_send_time = userdata['client_send_time']

    # Prepare the data to be logged into CSV
    data = {
        "client_send_time": client_send_time,  # Use the defined send time
        "network_time": 0.787,  # Assume constant network latency for demonstration
        "server_receive_time": float(result_data["server_receive_time"]),
        "image_save_time": float(result_data.get("image_save_time", result_data["server_receive_time"])),
        "image_preprocessed_time": float(result_data["image_preprocessed_time"]),
        "image_predicted_time": float(result_data["image_predicted_time"]),
        "qoe_computed_time": float(result_data.get("qoe_computed_time", result_data["image_predicted_time"])),
        "event_produced_time": float(result_data.get("event_produced_time", result_data["image_predicted_time"])),
        "response_create_time": float(result_data["response_create_time"]),
        "client_receive_time": client_receive_time
    }

    # Write the results to CSV
    with open('results.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'client_send_time', 'network_time', 'server_receive_time', 'image_save_time',
            'image_preprocessed_time', 'image_predicted_time', 'qoe_computed_time',
            'event_produced_time', 'response_create_time', 'client_receive_time'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only once
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)
        print(f"Request response logged to CSV.")

    client.loop_stop()  # Stop the MQTT loop after receiving a response


# Set up callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the result topic to listen for predictions
mqtt_client.subscribe(OUTPUT_TOPIC)

# Open the CSV file and prepare it for writing (initializing the file)
with open('results.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'client_send_time', 'network_time', 'server_receive_time', 'image_save_time',
        'image_preprocessed_time', 'image_predicted_time', 'qoe_computed_time',
        'event_produced_time', 'response_create_time', 'client_receive_time'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header to the CSV file

# Start the MQTT client and loop forever
mqtt_client.loop_forever()
