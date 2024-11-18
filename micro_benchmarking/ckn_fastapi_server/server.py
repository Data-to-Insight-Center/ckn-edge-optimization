import json
import os
import time
import logging
import traceback

import torch
from PIL import Image
from io import BytesIO

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from torchvision import transforms
from confluent_kafka import Producer
from werkzeug.utils import secure_filename

from model import predict, pre_process, model_store
from server_utils import save_file, process_qoe, check_file_extension

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the pre-trained model
MODEL = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v3_small', pretrained=True)
MODEL.eval()

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL = MODEL.to(device)

# Load labels
with open("imagenet_classes.txt", "r") as f:
    labels = [s.strip() for s in f.readlines()]

# Kafka producer setup
KAFKA_BROKER = os.getenv("CKN_KAFKA_BROKER", "149.165.170.250:9092")
RAW_EVENT_TOPIC = os.getenv("RAW_EVENT_TOPIC", "ckn_raw")
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def delivery_report(err, msg):
    """Kafka delivery report callback."""
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def pre_process(filename):
    """
    Pre-processes the image to allow the image to be fed into the PyTorch model.
    :param filename: Path to the image file.
    :return: Pre-processed image tensor.
    """
    input_image = Image.open(filename).convert("RGB")  # Ensure the image is in RGB format
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)
    return input_batch

def process_qoe(probability, compute_time, req_delay, req_accuracy):
    acc_qoe = min(1.0, req_accuracy / probability)
    delay_qoe = min(1.0, req_delay / compute_time)
    return 0.5 * acc_qoe + 0.5 * delay_qoe, acc_qoe, delay_qoe

# def save_file(file):
#     filename = secure_filename(file.filename)
#     file_path = os.path.join('./uploads', filename)
#     file.save(file_path)
#     while not os.path.exists(file_path):
#         time.sleep(0.1)
#     return file_path

@app.post("/predict/")
async def predict_endpoint(
    file: UploadFile = File(...),
    delay: float = Form(...),
    accuracy: float = Form(...)
):
    """Endpoint to process image and compute QoE."""
    server_receive_at = time.time()
    try:
        # Save file asynchronously
        filename = await save_file(file)
        image_save_at = time.time()

        # Preprocess and predict (assuming pre_process and predict are already async if necessary)
        preprocessed_input = pre_process(filename)  # Make sure pre_process is async if required
        image_preprocessed_at = time.time()

        prediction, probability = predict(preprocessed_input)  # Same for predict function
        image_predicted_at = time.time()

        # Compute QoE
        qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_at - server_receive_at, delay, accuracy)
        current_model_id = model_store.get_current_model_id()
        qoe_computed_at = time.time()

        # Kafka production (assuming you have a producer and topic setup)
        kafka_payload = json.dumps({
            'server_id': "", 'model_id': current_model_id,
            'qoe': qoe, 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe
        })
        producer.produce(RAW_EVENT_TOPIC, kafka_payload, callback=delivery_report)
        producer.flush(timeout=1)
        broker_produced_at = time.time()

        # Return response
        return JSONResponse(content={
            "model": "mobilenet_v3_small",
            "server_receive_at": server_receive_at,
            "image_save_at": image_save_at,
            "image_preprocessed_at": image_preprocessed_at,
            "image_predicted_at": image_predicted_at,
            "qoe_computed_at": qoe_computed_at,
            "broker_produced_at": broker_produced_at,
        })

    except Exception as e:
        error_message = str(e)
        stack_trace = traceback.format_exc()
        logging.error(f"Error processing prediction: {error_message}\n{stack_trace}")
        raise HTTPException(status_code=500, detail="Internal Server Error")