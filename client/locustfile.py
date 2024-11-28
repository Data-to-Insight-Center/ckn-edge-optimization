from locust import HttpUser, task, between, events, LoadTestShape
import time
import csv
import numpy as np

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

csv_filename = "results_locust_benchmark.csv"
fieldnames = [
    "client_send_time", "network_time", "server_receive_time", "image_save_time",
    "image_preprocessed_time", "image_predicted_time", "qoe_computed_time",
    "event_produced_time", "response_create_time", "client_receive_time"
]

with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


class QoEPredictUser(HttpUser):
    host = "http://149.165.174.52:8080"
    @task
    def send_qoe_predict_request(self):
        with open(file_location, 'rb') as file:
            files = {'file': (filename, file, 'image/jpeg')}
            client_send_time = time.perf_counter()

            with self.client.post("/predict", data=payload, files=files, catch_response=True) as response:
                client_receive_time = time.perf_counter()

                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        data = {
                            "client_send_time": client_send_time,
                            "network_time": 0.787,
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
                        with open(csv_filename, 'a', newline='') as csvfile_append:
                            writer = csv.DictWriter(csvfile_append, fieldnames=fieldnames)
                            writer.writerow(data)
                        response.success()
                    except ValueError:
                        response.failure("Invalid response format")
                        self.environment.runner.quit()  # Stop on first failure
                else:
                    response.failure(f"Failed with status code: {response.status_code}")
                    self.environment.runner.quit()  # Stop on first failure


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Test completed, results written to CSV.")


class StepLoadShape(LoadTestShape):
    step_time = 1  # Time in seconds before increasing user count
    step_load = 1  # Users to add per step
    spawn_rate = 1  # Users per second

    def __init__(self):
        super().__init__()
        self.user_count = 1
        self.max_users = 100

    def tick(self):
        run_time = self.get_run_time()
        if run_time < self.max_users * self.step_time:
            self.user_count = (run_time // self.step_time) * self.step_load + 1
            return self.user_count, self.spawn_rate
        return None
