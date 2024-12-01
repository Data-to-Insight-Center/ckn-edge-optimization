# Use a Python 3.11 base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the subscriber script
CMD python3 subscriber.py
