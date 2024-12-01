import json
import base64
import random
import os
import time
import csv
from paho.mqtt import client as mqtt_client

broker = '149.165.174.52'
port = 1883
topic = "camera-trap/predict"
client_id = f'mqtt_client_{random.randint(0, 1000)}'

# Variables for throughput measurement
message_count = 0
start_time = None
response_times = []

# CSV file to store results
csv_filename = "mqtt_performance_results.csv"


def connect_mqtt():
    """Connect to the MQTT broker."""

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker successfully!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    try:
        client.connect(broker, port)
    except Exception as e:
        print(f"Error connecting to MQTT Broker: {e}")
        return None
    return client


def publish(client):
    """Publish payload and file to the MQTT topic."""
    global message_count, start_time, response_times

    file_path = "abacus.jpg"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Metadata payload
    payload = {
        "accuracy": "0.849",
        "delay": "0.051",
        "server_id": "EDGE-1",
        "service_id": "imagenet_image_classification",
        "client_id": "raspi-1",
        "added_time": "03-04-2023 15:13:05",
        "ground_truth": "abacus"
    }

    # Encode file as Base64
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
        payload["file"] = encoded_file

    # Convert payload to JSON
    message = json.dumps(payload)

    # Measure response time
    start_response = time.perf_counter()  # Start timer
    result = client.publish(topic, message)
    end_response = time.perf_counter()  # End timer

    if result[0] == 0:
        print(f"Message sent to topic `{topic}` successfully.")
        response_time = (end_response - start_response) * 1000  # Convert to milliseconds
        response_times.append(response_time)
        print(f"Response Time: {response_time:.6f} ms")
    else:
        print(f"Failed to send message to topic `{topic}`.")

    # Increment message count
    if start_time is None:
        start_time = time.perf_counter()
    message_count += 1


def calculate_throughput():
    """Calculate and display throughput."""
    global start_time, message_count
    if start_time is not None:
        elapsed_time = time.perf_counter() - start_time
        throughput = message_count / elapsed_time
        return throughput
    return 0


def write_to_csv():
    """Write response times and throughput to a CSV file."""
    global response_times

    throughput = calculate_throughput()

    # Write results to CSV
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Message #", "Response Time (seconds)", "Throughput (messages/sec)"])
        for i, response_time in enumerate(response_times):
            writer.writerow([i + 1, response_time, throughput])  # Write each message's response time and throughput

    print(f"Results written to {csv_filename}")


def run():
    """Run the MQTT publisher."""
    client = connect_mqtt()
    if client:
        client.loop_start()

        # Publish the same message 1000 times
        for i in range(1000):  # Send 1000 messages
            publish(client)
            time.sleep(0.5)  # Adjust the interval if needed

        # Stop the client loop
        client.loop_stop()

        # Write the results to CSV after publishing all messages
        write_to_csv()


if __name__ == "__main__":
    run()
