# Ollama Command Cheat Sheet

This guide contains the most common commands for interacting with Ollama via the terminal and
API.

## 1. Basic Management Commands
These are the standard commands used to manage your local models and the environment.

| Command | Description | Example |
| :--- | :--- | :--- |
| `ollama serve` | Starts the Ollama server (usually runs automatically as a background service). | `ollama serve` |
| `ollama launch` | Used to start the application/service (context-dependent). | `ollama launch` |
| `ollama pull [model]` | Downloads a model from the library without running it. | `ollama pull llama3` |
| `ollama run [model]` | Downloads (if needed) and starts an interactive chat with the model. | `ollama run mistral` |
| `ollama list` | Lists all models currently installed on your machine. | `ollama list` |
| `ollama ls` | Lists files/models (often used as a shortcut for list). | `ollama ls` |
| `ollama rm [model]` | Removes a specific model from your local storage. | `ollama rm llama3` |
| `ollama show [model]` | Displays information about a specific model (parameters, system prompt). | `ollama show llama3` |
| `ollama create` | Create a new model based on a custom Modelfile. | `ollama create my-model -f Modelfile` |
| `ollama stop` | Stops the current process or service. | `ollama stop` |
| `ollama ps` | Lists active processes (useful to see what is running). | `ollama ps` |
| `ollama --version` | Displays the current version of Ollama installed. | `ollama --version` |
| `ollama help` / `-h` | Displays a list of all available commands and options. | `ollama -h` |

---

## 2. Common `ollama run` Arguments

The `run` command accepts several useful options to control model behavior.

| Argument | Description | Example |
| :--- | :--- | :--- |
| `--verbose` | Displays additional execution details (tokens, timings, debug information). | `ollama run llama3 --verbose` |
| `--think <true\|false>` | Enables or disables the model's reasoning mode (only for models that support thinking). | `ollama run qwen3 --think true` |
| `--hidethinking` | Hides the reasoning output while still allowing the model to reason internally. | `ollama run qwen3 --think true --hidethinking` |

---
*Note: Replace `llama3` with the specific model name you have downloaded.*

