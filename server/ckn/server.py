import json
import time
from confluent_kafka import Producer
from flask import Flask, request, jsonify

from utils import predict, pre_process, model_store, save_file, process_qoe, delivery_report
app = Flask(__name__)
producer = Producer({'bootstrap.servers': '149.165.170.250:9092'})

@app.route('/predict', methods=['POST'])
def qoe_predict():
    server_receive_time = time.perf_counter()

    file = request.files['file']
    data = request.form
    filename = save_file(file)
    image_save_time = time.perf_counter()

    preprocessed_input = pre_process(filename)
    image_preprocessed_time = time.perf_counter()

    prediction, probability = predict(preprocessed_input)
    image_predicted_time = time.perf_counter()

    qoe, acc_qoe, delay_qoe = process_qoe(probability, image_predicted_time - image_save_time, float(data['delay']), float(data['accuracy']))
    current_model_id = model_store.get_current_model_id()
    qoe_computed_time = time.perf_counter()

    kafka_payload = json.dumps({'model_id': current_model_id, 'qoe': qoe, 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe})
    producer.produce('ckn-event', kafka_payload, callback=delivery_report)
    producer.flush(timeout=1)
    event_produced_time = time.perf_counter()

    response = jsonify({
        "server_receive_time": server_receive_time,
        "image_save_time": image_save_time,
        "image_preprocessed_time": image_preprocessed_time,
        "image_predicted_time": image_predicted_time,
        "qoe_computed_time": qoe_computed_time,
        "event_produced_time": event_produced_time,
    })
    response.headers['response_create_time'] = time.perf_counter()

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)