# How to Use Ollama: A Comprehensive Guide

## 1. What is Ollama?
Ollama is an open-source framework designed to let users run large language models (LLMs)
locally on their own machine. It simplifies the process of setting up, running, and managing
models like Llama 3, Mistral, Phi-3, and many others.

## 2. Installation
To get started, you need to install Ollama based on your operating system:

*   **macOS:** Download the `.zip` from [ollama.com](https://ollama.com), extract it, and move
the application to your Applications folder.
*   **Linux:** Run the following command in your terminal:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
*   **Windows:** Download the installer from [ollama.com](https://ollama.com) and follow the
installation wizard.

## 3. Basic Commands
Once installed, you interact with Ollama primarily through your terminal (Command Prompt or
PowerShell on Windows).

### Run a model for the first time
To download and start chatting with a specific model (e.g., Llama 3), use:
```bash
ollama run llama3
```
*If the model is not already downloaded, Ollama will fetch it automatically before starting the
chat.*

### List available models on your machine
To see which models you have successfully downloaded:
```bash
ollama list
```

### Update or re-download a model
If you want to update a model or pull it without running it immediately:
```bash
ollama pull llama3
```

### Remove a model
To free up disk space by deleting a model you no longer use:
```bash
ollama rm mistral
```

## 4. Available Models
Ollama supports many models. Here are some popular ones:
- **Llama 3** (Meta) - Great all-rounder.
- **Mistral** - High performance for its size.
- **Phi-3** (Microsoft) - Lightweight and very fast.
- **Codellama** - Optimized for coding tasks.

To see the full list of available models, visit
[ollama.com/library](https://ollama.com/library).

## 5. Advanced Usage: Modelfiles
You can customize how a model behaves by creating a `Modelfile`. This allows you to set system
prompts and parameters (like temperature).

1. Create a file named `Modelfile`.
2. Add configuration:
   ```dockerfile
   FROM llama3
   PARAMETER temperature 0.7
   SYSTEM "You are a helpful assistant that speaks like a pirate."
   ```
3. Create the custom model:
   ```bash
   ollama create pirate-llama -f Modelfile
   ```
4. Run your new custom model:
   ```bash
   ollama run pirate-llama
   ```

## 6. Using the API
Ollama runs a local server by default on port **11434**. You can interact with it
programmatically using `curl` or any other programming language.

**Example of a simple API call:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

## 7. Useful Web Interfaces (Optional)
If you prefer a graphical user interface (GUI) instead of the terminal, you can connect Ollama
to:
- **Open WebUI** (The most popular UI, similar to ChatGPT).
- **Page Assist** (A Chrome/Firefox extension).
- **AnythingLLM**.

---
*Note: To use Ollama effectively, it is recommended to have at least 8GB of RAM for small models
and 16GB+ for larger ones.*