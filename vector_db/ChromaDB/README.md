# Multimodal Semantic Search using ChromaDB and CLIP (ViT-B/32)

This project implements a **multimodal semantic search system** using **ChromaDB** as a vector database and **Hugging Face’s CLIP (ViT-B/32)** model to store and retrieve **image and textual data** based on semantic similarity.

The system enables **cross-modal retrieval**, allowing users to search images using text queries and retrieve text using image queries.

---

## 🚀 Key Features

- ✅ Stores **image embeddings** and **text embeddings** in ChromaDB
- ✅ Uses **CLIP (ViT-B/32)** for unified image–text embedding space
- ✅ Supports **semantic similarity search**
- ✅ Handles **image captions + raw text**
- ✅ Metadata-rich storage for contextual filtering
- ✅ Efficient vector-based retrieval

---

## 🧠 Why CLIP + ChromaDB?

### CLIP (ViT-B/32)
- Trained on image–text pairs
- Maps images and text into the **same vector space**
- Enables **cross-modal semantic understanding**

### ChromaDB
- Lightweight and fast vector database
- Easy to store embeddings with metadata
- Ideal for **RAG**, **multimodal search**, and **AI pipelines**

---

## 🛠️ Tech Stack

- **Vector Database:** ChromaDB  
- **Embedding Model:** Hugging Face CLIP (ViT-B/32)  
- **Framework:** Python  
- **Image Processing:** Pillow (PIL)  
- **Text Processing:** Tokenization via CLIP  
- **Storage Type:** In-memory / persistent Chroma collections  

---

## 📂 Project Structure

- ├── image_data/ # Extracted images
- ├── text_data/ # Text chunks / captions
- ├── chroma_db/ # Chroma persistence directory
- ├── embed_and_store.py # Embedding + storage logic
- ├── search.py # Semantic search logic
- ├── requirements.txt
- └── README.md



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd chroma_multimodal_search

---

### 2️⃣ Create Virtual Environment
python -m venv venv

Activate

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate


### 3️⃣ Install Dependencies
pip install -r requirements.txt


---
### 🧩 Embedding & Storage Pipeline
####Image Data

- Images are loaded using PIL
- Encoded using CLIP image encoder
- Stored in a Chroma image collection

### Metadata includes:

- Image path
- Page number
- Caption
- Bounding box (if extracted from PDF)

### Text Data
- Text chunks or captions
- Encoded using CLIP text encoder
- Stored in a Chroma text collection


--- 
### 🧠 How Semantic Search Works
Query (Text / Image)
        ↓
CLIP Encoder
        ↓
Embedding Vector
        ↓
ChromaDB Similarity Search
        ↓
Top-K Most Similar Results

- Cosine similarity is used internally
- Both text and images are searchable across modalities



---
### 🔍 Example Searches
🔹 Text → Image Search

query = "diagram explaining attention mechanism"
results = image_collection.query(query_texts=[query], n_results=5)

🔹 Text → Text Search
query = "how transformer attention works"
results = text_collection.query(query_texts=[query], n_results=5)
 

### 🧪 Output Example
{
  "documents": [
    "Figure showing self-attention architecture"
  ],
  "metadatas": [
    {
      "image_path": "page_03_img_02.png",
      "caption": "Attention mechanism in transformers"
    }
  ],
  "distances": [0.21]
}

Lower distance → higher semantic similarity

--- 
### 📈 Use Cases

📄 PDF image–text retrieval
🧠 Multimodal RAG systems
🔍 Semantic document search
🖼️ Image search using natural language
📊 Research paper understanding

---
❗ Limitations

- CLIP ViT-B/32 is not OCR-based
- Very long documents require chunking
- Image caption quality affects retrieval accuracy

--- 
🎯 Future Improvements

- Add OCR-based text extraction
- Support hybrid search (keyword + vector)
- Add re-ranking using cross-encoders
- Integrate with FAISS for large-scale datasets


---  
### 🧠 Key Takeaway

This project demonstrates how multimodal embeddings and vector databases can be combined to build intelligent, semantic search systems capable of understanding both visual and textual information.


--- 
📌 Author

Aman Husain
GitHub: https://github.com/Aman-Husain-123
