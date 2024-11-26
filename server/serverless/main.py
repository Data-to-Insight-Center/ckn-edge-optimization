import time

from utils import predict, pre_process

if __name__ == '__main__':
    filename = "abacus.jpg"
    with open("serverless.csv", "w") as f:
        f.write("start_time,preprocess_time,predict_time\n")

        for i in range(1000):
            start_time = time.perf_counter()

            preprocessed_input = pre_process(filename)
            preprocess_time = time.perf_counter()

            prediction, probability = predict(preprocessed_input)
            predict_time = time.perf_counter()

            f.write(f"{start_time},{preprocess_time},{predict_time}\n")

