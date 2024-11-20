import csv
import time

import numpy as np
import requests

if __name__ == '__main__':
    host = "http://149.165.174.52:8080"
    filename = np.str_("abacus.jpg")
    file_location = "abacus.jpg"
    payload = {
        "accuracy": np.str_("0.849"),
        "delay": np.str_("0.051"),
        "server_id": np.str_("EDGE-1"),
        "service_id": np.str_("imagenet_image_classification"),
        "client_id": np.str_("raspi-1"),
        "added_time": np.str_("03-04-2023 15:13:05"),
        "ground_truth": "abacus"
    }

    csv_filename = "results_ckn.csv"

    # Updated fieldnames to include protocol latencies
    fieldnames = [
        "client_send_time", "network_time", "server_receive_time", "image_save_time",
        "image_preprocessed_time", "image_predicted_time", "qoe_computed_time",
        "event_produced_time", "response_create_time", "client_receive_time"
    ]

    # Open CSV file for writing data (new file every time)
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header at the start of the new file
        writer.writeheader()

        # Loop through 100 requests
        for i in range(1000):
            # Open the image file in binary mode
            with open(file_location, 'rb') as file:
                files = {
                    'file': (filename, file, 'image/jpeg')
                }

                # Measure client-side send and receive times
                client_send_time = time.perf_counter()
                response = requests.post(f"{host}/predict", data=payload, files=files)
                client_receive_time = time.perf_counter()

                # Calculate network time using `requests`
                network_time = (client_receive_time - client_send_time) - response.elapsed.total_seconds()

                # Parse server-side timings from the response JSON
                response_json = response.json()
                data = {
                    "client_send_time": client_send_time,
                    "network_time": network_time,
                    "server_receive_time": float(response_json["server_receive_time"]),
                    "image_save_time": float(response_json.get("image_save_time", float(response_json["server_receive_time"]))),
                    "image_preprocessed_time": float(response_json["image_preprocessed_time"]),
                    "image_predicted_time": float(response_json["image_predicted_time"]),
                    "qoe_computed_time": float(response_json.get("qoe_computed_time", float(response_json["image_predicted_time"]))),
                    "event_produced_time": float(response_json.get("event_produced_time", float(response_json["image_predicted_time"]))),
                    "response_create_time": float(response.headers["response_create_time"]),
                    "client_receive_time": client_receive_time
                }

                # Write individual request data to CSV
                writer.writerow(data)

            print(f"Request {i + 1} completed.")
