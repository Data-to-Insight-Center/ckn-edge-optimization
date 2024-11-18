FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files and folders from current directory to /app in container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Conditionally create the uploads directory
RUN mkdir -p /app/uploads

# Expose the port the app will run on (8080 for FastAPI)
EXPOSE 8080

# Use Uvicorn as the default ENTRYPOINT
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
