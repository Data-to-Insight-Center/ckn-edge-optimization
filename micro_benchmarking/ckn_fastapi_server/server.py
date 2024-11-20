import json
import logging
import os
import time

from confluent_kafka import Producer
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

from model import predict, pre_process, model_store
from server_utils import save_file, process_qoe

app = FastAPI()
SERVER_ID = os.getenv('SERVER_ID', 'd2iedgeai3')

KAFKA_BROKER = os.getenv("CKN_KAFKA_BROKER", "149.165.170.250:9092")
RAW_EVENT_TOPIC = os.getenv("RAW_EVENT_TOPIC", "ckn_events")
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def delivery_report(err, msg):
    """Kafka delivery report callback."""
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


@app.post("/predict/")
async def predict_endpoint(
    file: UploadFile = File(...),
    delay: float = Form(...),
    accuracy: float = Form(...)
):
    server_receive_time = time.perf_counter()

    filename = await save_file(file)
    image_save_time = time.perf_counter()

    preprocessed_input = pre_process(filename)
    image_preprocessed_time = time.perf_counter()

    prediction, probability = predict(preprocessed_input)
    image_predicted_time = time.perf_counter()

    # Compute QoE
    qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_time - server_receive_time, delay, accuracy)
    current_model_id = model_store.get_current_model_id()
    qoe_computed_time = time.perf_counter()

    # Kafka production
    kafka_payload = json.dumps({
        'server_id': SERVER_ID, 'model_id': current_model_id,
        'qoe': qoe, 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe
    })
    producer.produce(RAW_EVENT_TOPIC, kafka_payload, callback=delivery_report)
    producer.flush(timeout=1)
    event_produced_time = time.perf_counter()

    response = JSONResponse(content={
        "server_receive_time": server_receive_time,
        "image_save_time": image_save_time,
        "image_preprocessed_time": image_preprocessed_time,
        "image_predicted_time": image_predicted_time,
        "qoe_computed_time": qoe_computed_time,
        "event_produced_time": event_produced_time,
    })

    # Convert response_create_time to string before setting it in headers
    response_create_time = time.perf_counter()
    response.headers['response_create_time'] = str(response_create_time)

    return response