#!/usr/bin/env python3
"""
mentemo logs 用 RAG: 議事録・施策ログ・README・重要 data JSON を Chroma にインデックスする。
リポジトリルートで実行すること: python rag/index.py
"""
from pathlib import Path
import json
import os
import sys

# リポジトリルート = このスクリプトの親の親
RAG_DIR = Path(__file__).resolve().parent
REPO_ROOT = RAG_DIR.parent
CHROMA_DIR = RAG_DIR / ".chroma"
CACHE_DIR = RAG_DIR / ".cache"
COLLECTION_NAME = "mentemo"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def collect_chunks():
    """対象ファイルを走査し、(text, source, kind) のリストを返す。"""
    chunks = []
    root = REPO_ROOT

    # 議事録: ピッカーズ/施策ログ/data/議事録/*.json
    for p in sorted((root / "ピッカーズ/施策ログ/data/議事録").glob("*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            title = d.get("タイトル", "")
            date = d.get("日付", "")
            body = d.get("本文", "")
            supplement = d.get("補足", "")
            parts = [f"タイトル: {title}", f"日付: {date}", f"本文:\n{body}"]
            if supplement:
                parts.append(f"補足: {supplement}")
            text = "\n".join(parts)
            rel = str(p.relative_to(root))
            chunks.append((text, rel, "議事録"))
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)

    # 施策ログ: **/logs/*.jsonl（1行1チャンク）
    for p in sorted(root.glob("**/logs/*.jsonl")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        parts = [
                            d.get("日時", ""),
                            d.get("種別", ""),
                            d.get("概要", ""),
                            d.get("関連data", ""),
                        ]
                        text = " ".join(str(x) for x in parts if x)
                        rel = f"{p.relative_to(root)}#L{i}"
                        chunks.append((text, rel, "施策ログ"))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)

    # README: **/README.md（1ファイル1チャンク）
    for p in sorted(root.glob("**/README.md")):
        try:
            text = p.read_text(encoding="utf-8")
            rel = str(p.relative_to(root))
            chunks.append((text, rel, "README"))
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)

    # 重要 data: **/data/*.json（議事録ディレクトリ以外）
    for p in sorted(root.glob("**/data/*.json")):
        if "議事録" in str(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            text = _json_to_text(d)
            rel = str(p.relative_to(root))
            chunks.append((text, rel, "data"))
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)

    return chunks


def _json_to_text(obj, prefix=""):
    """JSON を読みやすいテキストに変換する。"""
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    if isinstance(obj, list):
        return "\n".join(_json_to_text(x, prefix) for x in obj)
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                parts.append(f"{k}:")
                parts.append(_json_to_text(v, prefix + "  "))
            else:
                parts.append(f"{k}: {_json_to_text(v)}")
        return "\n".join(parts)
    return str(obj)


def main():
    os.chdir(REPO_ROOT)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(CACHE_DIR))
    os.environ.setdefault("TRANSFORMERS_CACHE", str(CACHE_DIR))
    chunks = collect_chunks()
    if not chunks:
        print("対象ドキュメントがありません。", file=sys.stderr)
        sys.exit(1)

    print(f"埋め込みモデル読み込み: {EMBEDDING_MODEL}")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBEDDING_MODEL, cache_folder=str(CACHE_DIR))

    print(f"テキストをベクトル化 ({len(chunks)} 件)...")
    texts = [c[0] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    print("Chroma に保存...")
    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection(COLLECTION_NAME, metadata={"description": "mentemo logs RAG"})
    # 既存を削除してから追加（再インデックス）
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(COLLECTION_NAME, metadata={"description": "mentemo logs RAG"})

    ids = [f"doc_{i}" for i in range(len(chunks))]
    metadatas = [{"source": c[1], "kind": c[2]} for c in chunks]
    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
    )
    print(f"完了: {len(chunks)} 件を {CHROMA_DIR} に保存しました。")


if __name__ == "__main__":
    main()
