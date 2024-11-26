import time

from utils import predict, pre_process

if __name__ == '__main__':
    filename = 'abacus.jpg'
    with open("model_results.csv", "w") as f:
        f.write("preprocess_time,predict_time\n")

        for i in range(100):
            start_time = time.perf_counter()

            preprocessed_input = pre_process(filename)
            preprocess_time = time.perf_counter()

            prediction, probability = predict(preprocessed_input)
            predict_time = time.perf_counter()

            f.write(f"{preprocess_time - start_time},{predict_time - preprocess_time}\n")

