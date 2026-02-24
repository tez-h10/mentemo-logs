#!/usr/bin/env python3
"""
mentemo logs 用 RAG: 質問文で類似検索し、上位 K 件を表示する。
リポジトリルートで実行すること: python rag/query.py "質問文" [--top-k N]
"""
import argparse
import os
import sys
from pathlib import Path

RAG_DIR = Path(__file__).resolve().parent
REPO_ROOT = RAG_DIR.parent
CHROMA_DIR = RAG_DIR / ".chroma"
CACHE_DIR = RAG_DIR / ".cache"
COLLECTION_NAME = "mentemo"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_TOP_K = 5


def main():
    parser = argparse.ArgumentParser(description="mentemo RAG: 質問文で検索")
    parser.add_argument("query", nargs="+", help="質問文（スペース区切りで1つの文字列として扱う）")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help=f"取得件数 (default: {DEFAULT_TOP_K})")
    args = parser.parse_args()
    query_text = " ".join(args.query).strip()
    if not query_text:
        print("質問文を指定してください。", file=sys.stderr)
        sys.exit(1)

    os.chdir(REPO_ROOT)
    if CACHE_DIR.exists():
        os.environ.setdefault("HF_HOME", str(CACHE_DIR))
        os.environ.setdefault("TRANSFORMERS_CACHE", str(CACHE_DIR))
    if not CHROMA_DIR.exists():
        print(f"インデックスがありません。先に python rag/index.py を実行してください。", file=sys.stderr)
        sys.exit(1)

    print(f"埋め込みモデル読み込み: {EMBEDDING_MODEL}")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBEDDING_MODEL, cache_folder=str(CACHE_DIR))

    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        print("コレクションが見つかりません。先に python rag/index.py を実行してください。", file=sys.stderr)
        sys.exit(1)

    query_embedding = model.encode([query_text], show_progress_bar=False)[0]
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(args.top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if results.get("distances") else []

    if not docs:
        print("該当するドキュメントがありませんでした。")
        return

    for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances), 1):
        source = meta.get("source", "")
        kind = meta.get("kind", "")
        print(f"\n--- [{i}] {source} ({kind})" + (f" distance={dist:.4f}" if dist is not None else ""))
        print(doc[:2000] + ("..." if len(doc) > 2000 else ""))
    print()


if __name__ == "__main__":
    main()
