# ExplainableAI-Project2
 Social Explainability By Design

### Group Number: 1

### Teammates:
1. **Abhinav Atmuri**
2. **Bar Melinarskiy**
3. **Konstantinos Zavantias**
4. **Nikita Aksjonov**


#### In order to make mistral LLM running locally:
1. Go to https://hub.docker.com/r/ollama/ollama
2. Execute this command in the terminal -> docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama 
3. After you executed this command and container is running, run -> ollama pull mistral
4. You are ready to go and execute last files which include LLM explanations