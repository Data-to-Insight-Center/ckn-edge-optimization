import time
from flask import Flask, request, jsonify

from model import predict, pre_process
from server_utils import save_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/predict', methods=['POST'])
def qoe_predict():
    server_receive_time = time.perf_counter()

    file = request.files['file']
    filename = save_file(file)
    image_save_time = time.perf_counter()

    preprocessed_input = pre_process(filename)
    image_preprocessed_time = time.perf_counter()

    prediction, probability = predict(preprocessed_input)
    image_predicted_time = time.perf_counter()

    return jsonify({
        "server_receive_time": server_receive_time,
        "image_save_time": image_save_time,
        "image_preprocessed_time": image_preprocessed_time,
        "image_predicted_time": image_predicted_time
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)