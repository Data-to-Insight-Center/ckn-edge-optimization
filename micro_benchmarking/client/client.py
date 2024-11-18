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

    csv_filename = "results_flask.csv"

    fieldnames = ["model", "client_send_at", "server_receive_at",
                  "image_preprocessed_at", "image_predicted_at",
                  "image_save_at", "qoe_computed_at", "broker_produced_at", "client_receive_at"]

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

                client_send_at = time.time()
                response = requests.post(f"{host}/predict", data=payload, files=files)
                client_receive_at = time.time()

                response = response.json()
                # Prepare data for CSV row
                data = {
                    "model": response["model"],
                    "client_send_at": client_send_at,
                    "server_receive_at": float(response["server_receive_at"]),
                    "image_save_at": float(response.get("image_save_at", float(response["server_receive_at"]))),
                    "image_preprocessed_at": float(response["image_preprocessed_at"]),
                    "image_predicted_at": float(response["image_predicted_at"]),
                    "qoe_computed_at": float(response.get("qoe_computed_at", float(response["image_predicted_at"]))),
                    "broker_produced_at": float(response.get("broker_produced_at", float(response["image_predicted_at"]))),
                    "client_receive_at": client_receive_at
                }

                # Write individual request data to CSV
                writer.writerow(data)

            print(f"Request {i+1} completed.")