import json
import time
from confluent_kafka import Producer
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

from utils import predict, pre_process, model_store, save_file, process_qoe, delivery_report

app = FastAPI()
producer = Producer({'bootstrap.servers': '149.165.170.250:9092'})

@app.post("/predict")
def predict_endpoint(
    file: UploadFile = File(...),
    delay: float = Form(...),
    accuracy: float = Form(...)
):
    server_receive_time = time.perf_counter()

    filename = save_file(file)
    image_save_time = time.perf_counter()

    preprocessed_input = pre_process(filename)
    image_preprocessed_time = time.perf_counter()

    prediction, probability = predict(preprocessed_input)
    image_predicted_time = time.perf_counter()

    qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_time - server_receive_time, delay, accuracy)
    current_model_id = model_store.get_current_model_id()
    qoe_computed_time = time.perf_counter()

    kafka_payload = json.dumps({'model_id': current_model_id, 'qoe': qoe, 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe})
    producer.produce('ckn-event', kafka_payload, callback=delivery_report)
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

    response.headers['response_create_time'] = str(time.perf_counter())

    return response