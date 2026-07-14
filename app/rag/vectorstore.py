import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.rag.knowledge_base import MAINTENANCE_DOCS
import time

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
TOP_K_DEFAULT = 2
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score to include a result

# ─────────────────────────────────────────────
# Global State
# ─────────────────────────────────────────────
_model = None
_index = None
_doc_store = []
_is_built = False
_build_time = None

# ─────────────────────────────────────────────
# Model Loader (lazy loading — loads only when first needed)
# ─────────────────────────────────────────────
def _get_model():
    global _model
    if _model is None:
        print(f"[VectorStore] Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"[VectorStore] Model loaded successfully.")
    return _model


# ─────────────────────────────────────────────
# Build Vector Store
# ─────────────────────────────────────────────
def build_vectorstore():
    global _index, _doc_store, _is_built, _build_time

    print("[VectorStore] Building FAISS vector store from knowledge base...")
    start = time.time()

    model = _get_model()

    # Store full document metadata
    _doc_store = MAINTENANCE_DOCS

    # Extract text content for embedding
    texts = [
        f"{doc['title']}. {doc['content']}"
        for doc in MAINTENANCE_DOCS
    ]

    # Generate embeddings
    print(f"[VectorStore] Encoding {len(texts)} documents...")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
        normalize_embeddings=True  # Normalize for cosine similarity
    )

    # Build FAISS index (Inner Product = cosine similarity after normalization)
    dimension = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dimension)
    _index.add(embeddings.astype(np.float32))

    _is_built = True
    _build_time = time.time() - start

    print(f"[VectorStore] Vector store ready.")
    print(f"[VectorStore] Documents indexed: {len(texts)}")
    print(f"[VectorStore] Embedding dimension: {dimension}")
    print(f"[VectorStore] Build time: {_build_time:.2f}s")


# ─────────────────────────────────────────────
# Retrieve Relevant Documents
# ─────────────────────────────────────────────
def retrieve_docs(query: str, top_k: int = TOP_K_DEFAULT) -> list:
    global _index, _doc_store, _is_built

    # Auto-build if not already built
    if not _is_built:
        build_vectorstore()

    model = _get_model()

    print(f"[VectorStore] Retrieving docs for query: '{query[:60]}...'")

    # Encode query
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype(np.float32)

    # Search FAISS index
    scores, indices = _index.search(query_embedding, top_k)

    results = []
    for rank, (idx, score) in enumerate(zip(indices[0], scores[0])):
        if idx == -1:
            continue

        # Filter by similarity threshold
        if score < SIMILARITY_THRESHOLD:
            print(f"[VectorStore] Skipping doc {idx} — score {score:.3f} below threshold")
            continue

        doc = _doc_store[idx]
        results.append({
            "rank": rank + 1,
            "title": doc["title"],
            "topic": doc["topic"],
            "content": doc["content"].strip(),
            "similarity_score": round(float(score), 4)
        })

        print(f"[VectorStore] Match {rank+1}: '{doc['title']}' (score: {score:.3f})")

    print(f"[VectorStore] Retrieved {len(results)} relevant documents.")
    return results


# ─────────────────────────────────────────────
# Vector Store Status
# ─────────────────────────────────────────────
def get_vectorstore_status() -> dict:
    return {
        "is_built": _is_built,
        "total_documents": len(_doc_store) if _is_built else 0,
        "embedding_model": EMBEDDING_MODEL,
        "build_time_seconds": round(_build_time, 2) if _build_time else None
    }


# ─────────────────────────────────────────────
# Test (run directly)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    build_vectorstore()
    
    test_queries = [
        "engine temperature is too high",
        "oil pressure dropped below safe range",
        "battery voltage anomaly detected",
        "vehicle exceeding speed limit"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        results = retrieve_docs(query)
        for r in results:
            print(f"  [{r['rank']}] {r['title']} (score: {r['similarity_score']})")