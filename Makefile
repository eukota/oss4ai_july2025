# Variables
IMAGE_NAME = oss4ai-july2025
CONTAINER_NAME = oss4ai-july2025-container

#WEB_PORT = 5173

.PHONY: build run stop rm logs

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container
run:
	docker run -it \
		--name $(CONTAINER_NAME) \
		-v $(PWD)/src:/app \
		$(IMAGE_NAME)

# Stop the container (only needed for detached mode)
stop:
	docker stop $(CONTAINER_NAME)

# Remove the container
rm:
	docker rm $(CONTAINER_NAME)

# View logs
logs:
	docker logs -f $(CONTAINER_NAME)

start:
	docker start -ai $(CONTAINER_NAME)

clean:
	@echo "Stopping and removing container $(CONTAINER_NAME) if it exists..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
