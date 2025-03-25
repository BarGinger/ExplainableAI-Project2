# ExplainableAI-Project2: Social Explainability By Design

## Project Overview
This project focuses on generating natural language explanations for AI decision-making processes. It demonstrates how formal, technical explanations can be transformed into conversational, user-friendly explanations that are more accessible to non-technical users.

### Group Number: 1

### Team Members:
1. **Abhinav Atmuri**
2. **Bar Melinarskiy**
3. **Konstantinos Zavantias**
4. **Nikita Aksjonov**

## Getting Started

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Required Python packages (install via `pip install -r requirements.txt`):
  - anytree
  - numpy
  - pandas
  - requests

### Project Structure
- **`Part1/`** - Contains all code for the first part of the assignment regarding general goal tree explanations using anytree
- **`Part2/`** - Natural language explanations for decisions made by the agent in the goal tree
  - `nl_generation.ipynb`: Jupyter notebook for generating natural language explanations
  - `ollama_docker/ollama.yaml`: Docker configuration for the language model
- **`generate_explanations_for_test_cases.py`**: Generates baseline technical explanations
- **`requirements.txt`**: List of required Python packages

## Running the Project

### Step 1: Generate Baseline Explanations
Run the following command to generate the initial technical explanations:
```bash
python generate_explanations_for_test_cases.py
```

### Step 2: Set Up the Language Model
Start the Docker container with the language model (Mistral):
```bash
docker-compose -f ./Part2/ollama_docker/ollama.yaml up --build -d
```

### Step 3: Generate Natural Language Explanations
Open and run the Jupyter notebook:
```bash
jupyter notebook Part2/nl_generation.ipynb
```

## Explanation Output
The generated explanations will be saved in:
- `explanations/baseline/`: Technical explanations
- `explanations/llama3/` or `explanations/mistral/`: Natural language explanations

## Shutting Down
To stop the Docker container when finished:
```bash
docker-compose -f ./Part2/ollama_docker/ollama.yaml down
```

## Project Description
This project demonstrates how AI systems can provide more human-friendly explanations of their decision-making processes. By transforming formal reasoning codes and technical explanations into natural language, we make AI decisions more transparent and accessible to non-technical users.