from locust import HttpUser, task, between, events
import time
import csv
import numpy as np

# Define file and payload details for the POST request
filename = np.str_("abacus.jpg")
file_location = "abacus.jpg"
payload = {
    "accuracy": np.str_("0.849"),
    "delay": np.str_("0.051"),
    "server_id": np.str_("EDGE-1"),
    "service_id": np.str_("imagenet_image_classification"),
    "client_id": np.str_("raspi-1"),
    "added_time": np.str_("03-04-2023 15:13:05"),
    "ground_truth": "abacus"  # Adding ground_truth if required
}

# Initialize a CSV file to log performance data
csv_filename = "results_locust_benchmark.csv"
fieldnames = [
    "client_send_time", "network_time", "server_receive_time", "image_save_time",
    "image_preprocessed_time", "image_predicted_time", "qoe_computed_time",
    "event_produced_time", "response_create_time", "client_receive_time"
]

# Open CSV file for writing data (new file every time)
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write header at the start of the new file


    class QoEPredictUser(HttpUser):
        host = "http://149.165.174.52:8080"
        @task
        def send_qoe_predict_request(self):
            # Open the image file in binary mode
            with open(file_location, 'rb') as file:
                files = {
                    'file': (filename, file, 'image/jpeg')
                }

                # Measure client-side send and receive times
                client_send_time = time.perf_counter()

                # Perform the POST request using Locust's client
                with self.client.post("/predict", data=payload, files=files, catch_response=True) as response:
                    client_receive_time = time.perf_counter()

                    # Calculate network time using response's elapsed time
                    network_time = (client_receive_time - client_send_time) - response.elapsed.total_seconds()

                    # Parse server-side timings from the response JSON
                    try:
                        response_json = response.json()
                    except ValueError:
                        response.failure("Invalid response format")
                        return

                    # Extract timings from the server response
                    data = {
                        "client_send_time": client_send_time,
                        "network_time": network_time,
                        "server_receive_time": float(response_json["server_receive_time"]),
                        "image_save_time": float(
                            response_json.get("image_save_time", float(response_json["server_receive_time"]))),
                        "image_preprocessed_time": float(response_json["image_preprocessed_time"]),
                        "image_predicted_time": float(response_json["image_predicted_time"]),
                        "qoe_computed_time": float(
                            response_json.get("qoe_computed_time", float(response_json["image_predicted_time"]))),
                        "event_produced_time": float(
                            response_json.get("event_produced_time", float(response_json["image_predicted_time"]))),
                        "response_create_time": float(response.headers.get("response_create_time", 0)),
                        "client_receive_time": client_receive_time
                    }

                    # Write the individual request data to the CSV file
                    with open(csv_filename, 'a', newline='') as csvfile_append:
                        writer = csv.DictWriter(csvfile_append, fieldnames=fieldnames)
                        writer.writerow(data)

                    # Mark the request as successful if the response is 200
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Failed with status code: {response.status_code}")


    # Event listener to stop the test gracefully
    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print("Test completed, results written to CSV.")