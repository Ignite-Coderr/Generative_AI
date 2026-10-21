# 🚀 Quick Start Guide - Intelligent Model Router

## Step 1: Install Dependencies

Open terminal and run:

```bash
cd c:\Users\user\OneDrive\Documents\Generative_AI\RAG_Practice\LLM_Router
pip install -r requirements.txt
```

**Note:** First installation may take 5-10 minutes as it downloads the embedding model.

## Step 2: Run the Application

```bash
streamlit run streamlit_app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## Step 3: Try Example Queries

Once the app loads, try these examples:

### 🔢 Basic Math
```
2 + 3
```
**Expected:** Routes to Small-Math model

### 🧮 Advanced Math
```
Solve differential equation dy/dx = x^2
```
**Expected:** Routes to DeepSeek-Math model

### 📚 Explanation
```
Explain transformer architecture in detail
```
**Expected:** Routes to Research-GPT model

### 🎭 Creative
```
Roast me
```
**Expected:** Routes to Roast-GPT model

## Docker Alternative

If you prefer Docker:

```bash
# Build image
docker build -t model-router .

# Run container
docker run -p 8501:8501 model-router
```

## Troubleshooting

### Issue: Module not found
**Solution:** Make sure you're in the correct directory and have activated your virtual environment (if using one)

### Issue: Port already in use
**Solution:** Use a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Slow first load
**Solution:** This is normal - the embedding model downloads on first run (~90MB). Subsequent runs will be fast.

## What to Expect

1. **Initialization** (~10-20 seconds on first run)
   - Loading embedding model
   - Building FAISS index
   - Registering models

2. **Query Processing** (~1-2 seconds)
   - Intent detection
   - Embedding generation
   - Similarity search
   - Response generation

3. **Results Display**
   - Selected model name
   - Confidence level
   - Routing analysis
   - Model response

## Next Steps

- Explore the codebase in the `app/` directory
- Read the comprehensive README.md
- Modify model descriptions to test routing changes
- Experiment with custom queries
- Integrate actual model APIs (OpenAI, Anthropic, etc.)

Enjoy your intelligent model router! 🎉
