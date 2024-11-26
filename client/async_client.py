import csv
import time
import numpy as np
import aiohttp
import aiofiles
import asyncio


async def send_request(session, host, filename, file_location, payload, csv_writer):
    """
    Function to send a single request and log the results to a CSV file asynchronously.
    """
    # Open the image file in binary mode asynchronously
    async with aiofiles.open(file_location, 'rb') as file:
        # Create a FormData object for the file and other fields
        form_data = aiohttp.FormData()
        form_data.add_field('file', file, filename=filename, content_type='image/jpeg')

        # Add additional fields from payload
        for key, value in payload.items():
            form_data.add_field(key, value)

        client_send_at = time.time()

        # Make the POST request
        async with session.post(f"{host}/predict", data=form_data) as response:
            client_receive_at = time.time()

            response_data = await response.json()

            # Prepare data for CSV row
            data = {
                "model": response_data["model"],
                "client_send_at": client_send_at,
                "server_receive_at": float(response_data["server_receive_at"]),
                "image_save_at": float(response_data.get("image_save_at", float(response_data["server_receive_at"]))),
                "image_preprocessed_at": float(response_data["image_preprocessed_at"]),
                "image_predicted_at": float(response_data["image_predicted_at"]),
                "qoe_computed_at": float(
                    response_data.get("qoe_computed_at", float(response_data["image_predicted_at"]))),
                "broker_produced_at": float(
                    response_data.get("broker_produced_at", float(response_data["image_predicted_at"]))),
                "client_receive_at": client_receive_at
            }

            # Write individual request data to CSV asynchronously
            csv_writer.writerow(data)

        print(f"Request completed.")


async def main():
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

    csv_filename = "results_fastapi_ckn.csv"

    fieldnames = ["model", "client_send_at", "server_receive_at",
                  "image_preprocessed_at", "image_predicted_at",
                  "image_save_at", "qoe_computed_at", "broker_produced_at", "client_receive_at"]

    # Open CSV file for writing data (new file every time)
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header at the start of the new file
        writer.writeheader()

        # Create an aiohttp session
        async with aiohttp.ClientSession() as session:
            # Loop through 1000 requests concurrently
            tasks = []
            for i in range(1000):
                task = send_request(session, host, filename, file_location, payload, writer)
                tasks.append(task)

            # Wait for all requests to complete
            await asyncio.gather(*tasks)


# Run the async main function
if __name__ == '__main__':
    asyncio.run(main())
