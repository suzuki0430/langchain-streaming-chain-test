# Implementation of Real-Time Display with LangChain and LLM

This project implements a method to display responses from AI chatbots in real-time using LangChain and Large Language Models (LLM). By utilizing Docker, the project simplifies environment setup and ensures consistent execution results across different environments.

## Execution Instructions

### Setting Environment Variables

1. Create a `.env` file in the root directory.
2. Set your OpenAI API key to `OPENAI_API_KEY`.

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Building the Docker Image

Build the Docker image. Please execute this command in the project's root directory.

```bash
docker build -t langchain-streaming-chain-test .
```

### Launching the Container

Next, mount the current directory on the host machine (local environment) to `/usr/src/app` in the container, and start the container. This allows changes made locally to be reflected inside the container.

```bash
docker run --env-file .env -v $(pwd):/usr/src/app -it langchain-streaming-chain-test
```

### Executing the Script

Once the bash shell in the container is up, run the script with the following command.

```bash
python main.py
```
