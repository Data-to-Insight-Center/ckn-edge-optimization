import time

import torch

from model import predict, pre_process

MODEL = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v3_small', pretrained=True)
MODEL.eval()

# Load labels
with open("imagenet_classes.txt", "r") as f:
    LABELS = [s.strip() for s in f.readlines()]

if __name__ == '__main__':
    filename = 'abacus.jpg'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # write the results to a csv
    with open("model_results.csv", "w") as f:
        f.write("preprocess_time,predict_time\n")

        # Loop through 100 requests
        for i in range(100):

            start_time = time.perf_counter()
            preprocessed_input = pre_process(filename).to(device)
            preprocess_time = time.perf_counter()
            prediction, probability = predict(preprocessed_input)
            predict_time = time.perf_counter()

            f.write(f"{preprocess_time - start_time},{predict_time - preprocess_time}\n")

