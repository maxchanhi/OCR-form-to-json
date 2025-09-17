# OCR Form to JSON

This project uses a multimodal large language model to perform Optical Character Recognition (OCR) on images of forms and extracts the information into a structured JSON format.

## Installation

Follow these steps to set up the project environment.

### 1. Clone the Repository

```bash
git clone https://github.com/maxchanhi/OCR-form-to-json.git
cd OCR-form-to-json
```

### 2. Install Dependencies

This project uses `uv` for package management.

First, install `uv`:

```bash
pip install uv
```

Then, create a virtual environment and install the project dependencies:

```bash
uv venv
uv pip sync pyproject.toml
```

### 3. Install Ollama and Pull the Model

You need to have Ollama installed to run the multimodal model.

- **Install Ollama**: Follow the instructions on the [Ollama website](https://ollama.com/).

- **Pull the model**: Once Ollama is installed and running, pull the `qwen2.5vl` model:

  ```bash
  ollama pull qwen2.5vl
  ```

## Usage

To run the OCR process, execute the `fill.py` script from the root of the project:

```bash
python orc/fill.py
```

The script will:
1. Process all images in the `orc/img/` directory.
2. Use the `qwen2.5vl` model to extract information based on the template in `orc/json_template/`.
3. Save the extracted JSON data into the `orc/result/` directory.