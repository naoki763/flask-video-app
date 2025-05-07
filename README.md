# 動画鑑賞アプリ

このアプリは、利用者が動画を投稿、閲覧し、コメントを通じてコミュニケーションを図ることができる動画ストリーミングプラットフォームです。また、管理者は効率的に利用者および動画を管理できます。

## 機能一覧

### 利用者管理
- **登録機能**: 新規利用者の登録
- **情報編集**: 利用者情報の編集
- **削除機能**: 利用者の削除

### ログイン機能
- **ログイン・ログアウト**: 利用者認証

### 動画管理
- **動画アップロード**: AWS S3への動画保存
- **動画閲覧**: 投稿動画の視聴
- **動画削除**: 不要な動画を削除（管理者のみ）

### コメント機能
- **コメント投稿**: 動画へのコメント投稿
- **コメント返信**: 投稿されたコメントへの返信

## 技術スタック

- **バックエンド**
  - 言語: Python 3.12
  - フレームワーク: Flask
  - ORM: SQLAlchemy

- **フロントエンド**
  - テンプレートエンジン: Jinja2
  - HTML/CSS, JavaScript

- **データベース**
  - PostgreSQL (AWS RDS)

- **インフラ**
  - terraform(インフラのIaC化)
  - AWS ECS（アプリケーションのホスティング）
  - AWS S3（動画保存）
  - AWS RDS（データベース）
  

- **開発ツール・環境**
  - Docker & Docker Compose
  - LocalStack（AWSサービスのローカルエミュレーション）
  - Visual Studio Code

## プロジェクト構成

```
video-streaming-app/
├── app/
│   ├── api/             # APIエンドポイント
│   ├── models/          # データベースモデル
│   ├── templates/       # Jinja2テンプレート
│   ├── static/          # CSS, JS, 画像
│   ├── config.py        # アプリケーション設定
│   ├── factory.py       # Flaskアプリ作成
│   ├── main.py          # アプリケーション起動
│   └── run.py           # 開発用サーバー実行スクリプト
├── tests/               # テストスクリプト
├── docker/              # Docker設定
├── .env                 # 環境変数管理
├── pyproject.toml       # プロジェクト設定
└── README.md
```

## 使用方法

### セットアップ

1. 仮想環境作成
```bash
python -m venv venv
```

2. パッケージインストール
```bash
pip install -r requirements.txt
```

3. DockerでLocalStack起動
```bash
docker-compose up
```

### データベースマイグレーション
```bash
flask db upgrade
```

### アプリケーション起動
```bash
flask run
```

