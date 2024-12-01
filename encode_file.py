import base64

with open("/Users/neeleshkarthikeyan/d2i/ckn-edge-optimization/client/abacus.jpg", "rb") as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')

with open("encoded_file.txt", "w") as output:
    output.write(encoded_string)
