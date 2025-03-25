# Stage 1: Base image
FROM ollama/ollama as base

# Copy your Modelfile into the container
COPY Modelfile /Modelfile

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]