# Project Name

This project is a Python-based application developed using modern tooling.

⚠️ **Note:** The dataset is **not included** in this repository.

---

## 🖥️ System Configuration

The project was developed and tested using the following setup:

- **Operating System:** Windows 11  
- **CUDA Toolkit:** 13.1  

⚠️ **GPU Acceleration Notice**

The current configuration **does not support GPU acceleration** with TensorFlow.  
To enable GPU support with **TensorFlow 2.8**, the following versions are required:
- **CUDA Toolkit:** 11.2  
- **cuDNN:** 8.1  

The current CUDA version (**13.1**) is **not compatible** with TensorFlow 2.8 GPU support.

As a result, the project runs correctly on **CPU only**.  
You can safely ignore GPU-related warnings displayed in the terminal.


---

## 📦 Installation

This project uses `uv` for dependency management.

1. Install dependencies:  
    ```bash 
    uv sync
    ```


2. Run the project:
    ```bash 
    uv run .\main.py
    ```


📊 Dataset

The dataset is not included in this repository.
You will need to:  
Download or prepare the dataset separately  
Place it in the appropriate directory (according to your local setup)  
This is intentional to keep the repository lightweight and avoid distributing large files.
The dataset is present in the original repo:
(https://github.com/nicknochnack/ImageClassification)
  
📝 Notes

The virtual environment (.venv) is intentionally excluded from version control.
Dependency versions are locked using uv.lock for reproducibility.