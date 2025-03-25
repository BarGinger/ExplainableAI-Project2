#!/bin/sh

# Start the Ollama app in the background
ollama serve &

# Wait for the Ollama app to be ready
sleep 10

# Pull the base model and create a new custom model
ollama pull llama3
ollama create custom-llama3 -f /ModelfileLlama3

# Pull the base model and create a new custom model
ollama pull mistral
ollama create custom-mistral -f /ModelFileMistral

# Keep the container running
tail -f /dev/null