import json
import os
import time

from confluent_kafka import Producer
from flask import Flask, flash, request, redirect, jsonify

from model import predict, pre_process, model_store
from server_utils import save_file, process_qoe, check_file_extension

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
SERVER_ID = os.getenv('SERVER_ID', 'd2iedgeai3')

KAFKA_BROKER = os.getenv('CKN_KAFKA_BROKER', '149.165.170.250:9092')

RAW_EVENT_TOPIC = os.getenv('RAW_EVENT_TOPIC', 'ckn_events')
START_DEPLOYMENT_TOPIC = os.getenv('START_DEPLOYMENT_TOPIC', 'ckn_start_deployment')
END_DEPLOYMENT_TOPIC = os.getenv('END_DEPLOYMENT_TOPIC', 'ckn_end_deployment')

producer = Producer({'bootstrap.servers': KAFKA_BROKER})
previous_deployment_id = None
last_model_id = None
deployment_id = None

def delivery_report(err, msg):
    """
    Delivery report callback function.
    :param err: Delivery error (if any).
    :param msg: Message object.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

@app.route('/predict', methods=['POST'])
def qoe_predict():
    """
    Prediction endpoint.
    """
    file = request.files['file']
    data = request.form

    server_receive_at = time.time()
    filename = save_file(file)
    image_save_at = time.time()

    preprocessed_input = pre_process(filename)
    image_preprocessed_at = time.time()

    prediction, probability = predict(preprocessed_input)
    image_predicted_at = time.time()

    qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_at - image_save_at, float(data['delay']), float(data['accuracy']))
    current_model_id = model_store.get_current_model_id()
    qoe_computed_at = time.time()

    kafka_payload = json.dumps({'server_id': SERVER_ID, 'model_id': current_model_id, 'qoe': qoe, 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe})
    producer.produce(RAW_EVENT_TOPIC, kafka_payload, callback=delivery_report)
    producer.flush(timeout=1)
    broker_produced_at = time.time()

    return jsonify({
        "model": "mobilenet_v3_small",
        "server_receive_at": server_receive_at,
        "image_save_at": image_save_at,
        "image_preprocessed_at": image_preprocessed_at,
        "image_predicted_at": image_predicted_at,
        "qoe_computed_at": qoe_computed_at,
        "broker_produced_at": broker_produced_at,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)