import os
import time
import aiofiles
from werkzeug.utils import secure_filename

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def process_qoe(probability, compute_time, req_delay, req_accuracy):
    acc_qoe = min(1.0, req_accuracy / probability)
    delay_qoe = min(1.0, req_delay / compute_time)
    return 0.5 * acc_qoe + 0.5 * delay_qoe, acc_qoe, delay_qoe

def check_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

UPLOAD_FOLDER = './uploads'
async def save_file(file):
    """Asynchronously save the uploaded file to disk."""
    filename = secure_filename(file.filename)  # Secure the filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    async with aiofiles.open(file_path, 'wb') as f:
        # Read the file in chunks and write asynchronously
        chunk_size = 1024 * 1024  # 1MB chunks (adjust as needed)
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            await f.write(chunk)

    return file_path
