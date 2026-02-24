# GitHub（mentemo logs）へのプッシュ手順

リポジトリは **~/Desktop/AI** がルートです。リポジトリ名: **mentemo logs**（URL では `mentemo-logs`）。

## 1. GitHub でリポジトリを作る

1. [GitHub New repository](https://github.com/new) を開く
2. リポジトリ名: **mentemo-logs**
3. Public / Private を選択（README 等は追加しない）
4. **Create repository** をクリック

## 2. リモートを追加してプッシュ

```bash
cd ~/Desktop/AI
git remote add origin https://github.com/<ユーザー名>/mentemo-logs.git
git push -u origin main
```

SSH の場合:

```bash
git remote add origin git@github.com:<ユーザー名>/mentemo-logs.git
git push -u origin main
```

## GitHub CLI の場合

```bash
cd ~/Desktop/AI
gh repo create mentemo-logs --public --source=. --push
```

---

## 今後の更新

```bash
cd ~/Desktop/AI
git add .
git commit -m "施策ログを更新"
git push
```
