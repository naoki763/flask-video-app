# 動画鑑賞アプリ

このアプリは、利用者が動画を投稿、閲覧し、コメントを通じてコミュニケーションを図ることができる動画ストリーミングプラットフォームです。また、管理者は効率的に利用者および動画を管理できます。

## 前提条件
このアプリの開発環境はVisual Studio Codeでの開発を前提としています。
ご利用前に以下がホストPCにインストールしてください
  * Visual Studio Code
  * Docker(Version2推奨)

また、Visual Studio Codeインストール後、以下の『Dev Containers』拡張機能を追加してください。
  * ms-vscode-remote.remote-containers

## 機能一覧

### 利用者管理

* **登録機能**: 新規利用者の登録
* **情報編集**: 利用者情報の編集
* **削除機能**: 利用者の削除

### ログイン機能

* **ログイン・ログアウト**: 利用者認証

### 動画管理

* **動画アップロード**: AWS S3への動画保存
* **動画閲覧**: 投稿動画の視聴
* **動画削除**: 不要な動画を削除

### コメント機能

* **コメント投稿**: 動画へのコメント投稿
* **コメント返信**: 投稿されたコメントへの返信

## 技術スタック

* **バックエンド**

  * 言語: Python 3.12
  * フレームワーク: Flask
  * ORM: SQLAlchemy

* **フロントエンド**

  * テンプレートエンジン: Jinja2
  * HTML/CSS, JavaScript

* **データベース**

  * PostgreSQL (AWS RDS)

* **インフラ**

  * terraform（インフラのIaC化）
  * AWS ECS（アプリケーションのホスティング）
  * AWS S3（動画保存）
  * AWS RDS（データベース）

* **開発ツール・環境**

  * Docker & Docker Compose
  * LocalStack
  * Visual Studio Code
  * uv
  * mise
  * go-task

## 開発環境詳細

### Dev Container

VSCodeの開発環境をDockerで管理し、プロジェクト毎に独立した開発環境を構築可能にします。

### uv

高速なPythonパッケージマネージャで、パッケージのインストールや仮想環境管理を効率的に行えます。

```bash
uv venv
uv pip install -r requirements.txt
```

### mise

開発で使用するツールのバージョンを管理するためのツールで、環境ごとに異なるバージョンを指定できます。

```bash
mise use python@3.12
```

### ruff

Pythonコードのリンティングとフォーマットを高速に行うツールです。

```bash
ruff check .
ruff format .
```

### go-task

タスクを簡単に自動化・管理するためのシンプルで強力なツールです。

```bash
task run
```

### localstack

AWSのサービスをローカル環境でエミュレートするためのツールで、AWS依存の開発をローカル環境で安全に実施できます。

```bash
docker-compose up
```

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

## 開発環境利用方法

### セットアップ

1. DevContainerを開く.
  - VSCodeのコマンドパレットを開き「Dev Containers: Reopen in Container」を選択する。

2. LocalStackなどインフラ立ち上げ
vscodeのターミナルを開き、以下のコマンドを実行する

```bash
task dev-config
```

3. アプリ起動

```bash
task app-start
```
