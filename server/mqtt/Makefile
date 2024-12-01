# Variables
DOCKER_IMAGE_NAME=mqtt-ckn-daemon
DOCKER_CONTAINER_NAME=mqtt-daemon
DOCKERFILE_PATH=./Dockerfile
COMPOSE_FILE=docker-compose.yml

# Default target
all: build run

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) -f $(DOCKERFILE_PATH) .

# Run the Docker container
run:
	docker run -d --name $(DOCKER_CONTAINER_NAME) \
		-p 1883:1883 \
		-p 8080:8080 \
		$(DOCKER_IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(DOCKER_CONTAINER_NAME)

# Remove the Docker container
remove:
	docker rm $(DOCKER_CONTAINER_NAME)

# Remove the Docker image
remove-image:
	docker rmi $(DOCKER_IMAGE_NAME)

# Clean up - stop, remove container, and remove image
clean: stop remove remove-image
