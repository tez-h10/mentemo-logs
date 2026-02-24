# mentemo logs 用 RAG

議事録・施策ログ・README・重要 data JSON を対象に、自然言語で検索できる小型 RAG です。  
埋め込みは **sentence-transformers**（API キー不要）、ベクトル保存は **ChromaDB** を使用します。

## 使い方

リポジトリルート（`mentemo logs` のルート）で以下を実行してください。

### 1. 環境準備

```bash
cd /path/to/mentemo-logs   # リポジトリルート
pip install -r rag/requirements.txt
```

（推奨）venv を使う場合:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r rag/requirements.txt
```

### 2. インデックス作成

```bash
python rag/index.py
```

初回は sentence-transformers のモデルダウンロードで少し時間がかかります。  
完了すると `rag/.chroma/` にベクトルが保存されます。

### 3. 質問で検索

```bash
python rag/query.py "ピッカーズの残タスクは？"
python rag/query.py "エザキのLP一覧" --top-k 3
```

- `--top-k N` で取得件数（デフォルト 5）を指定できます。

## 対象データ

| 種別 | パス | チャンク |
|------|------|----------|
| 議事録 | `ピッカーズ/施策ログ/data/議事録/*.json` | 1ファイル＝1件 |
| 施策ログ | 各案件の `**/logs/*.jsonl` | 1行＝1件 |
| README | `**/README.md` | 1ファイル＝1件 |
| 重要 data | `**/data/*.json`（議事録フォルダ内を除く） | 1ファイル＝1件 |

議事録・ログ・README を追加・更新したら、**再度 `python rag/index.py` を実行**してから検索してください。

## 注意

- インデックスは `rag/.chroma/` に保存されます。モデルキャッシュは `rag/.cache/` に保存します。いずれも `.gitignore` で除外しています。
- 初版では「検索結果のテキストをそのまま表示」のみです。要約・回答生成は未実装です。
