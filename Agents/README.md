# Agents Project

LangChain agents project with Euron AI integration.

## Setup

### Prerequisites
- Python 3.10

### Installation

1. Create virtual environment:
```bash
py -3.10 -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Register Jupyter kernel:
```bash
python -m ipykernel install --user --name=agents_py310 --display-name="Python 3.10 (Agents)"
```

### Configuration

1. The API key is stored in `.env` file (already configured)
2. The notebook automatically loads the API key from `.env`
3. If you need to change the API key, edit the `.env` file:
```
EURON_API_KEY=your_api_key_here
```

**Note:** The `.env` file is excluded from git for security.

## Usage

1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `index.ipynb`
3. Select kernel: **Python 3.10 (Agents)**
4. Run the cells

## Packages Installed

- **langchain** - LangChain framework
- **langchain-core** - Core LangChain components
- **langchain-community** - Community integrations
- **euriai** - Euron AI integration
- **pydantic** - Data validation (v2.12.5)
- **jupyter** - Jupyter notebook
- **ipykernel** - Jupyter kernel

## Notes

- Python 3.10 is required for compatibility
- Pydantic v2.x is used for compatibility with both LangChain and euriai
- The virtual environment is excluded from git via `.gitignore`
