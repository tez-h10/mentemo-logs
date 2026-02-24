# GitHub に上げる手順

このフォルダはすでに **git リポジトリ**になっています（初回コミット済み）。

## 1. GitHub で新しいリポジトリを作る

1. [GitHub](https://github.com/new) で **New repository** を開く
2. リポジトリ名を入力（例: `pickers` または `ピッカーズ`）
3. **Public** を選択（Private でも可）
4. **README や .gitignore は追加しない**（ローカルに既にあるため）
5. **Create repository** をクリック

## 2. リモートを追加してプッシュ

GitHub で表示される「…or push an existing repository from the command line」のコマンドを実行します。

```bash
cd /Users/user/AI/ピッカーズ
git remote add origin https://github.com/<あなたのユーザー名>/<リポジトリ名>.git
git push -u origin main
```

または SSH を使う場合:

```bash
git remote add origin git@github.com:<あなたのユーザー名>/<リポジトリ名>.git
git push -u origin main
```

## GitHub CLI を使う場合

`gh` が入っていれば、リポジトリ作成とプッシュをまとめて実行できます。

```bash
cd /Users/user/AI/ピッカーズ
gh repo create pickers --public --source=. --push
```

---

以降、内容を更新したら以下で GitHub に反映できます。

```bash
cd /Users/user/AI/ピッカーズ
git add .
git commit -m "施策ログを更新"
git push
```
