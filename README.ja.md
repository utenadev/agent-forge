# Agent Forge

**Agent Forge** は、tmux を活用した「OSレベルのマルチエージェント・オーケストレーション基盤」です。
手続き的なシェルスクリプトではなく、**tmuxp** (YAML) と **libtmux** (Python) を用いることで、宣言的かつプログラマブルな「エージェントの仕事場」を構築します。

## 特徴: "Forge Link" プロトコル

エージェント間の連携プロトコル **Forge Link** を実装しています。

1.  **宣言的環境 (The Forge)**:
    YAML ファイル (`.forge.yaml`) で定義される、役割分担が明確なワークスペース。
    - **Architect Pane**: 設計、構造定義
    - **Implementer Pane**: 実装、コーディング
    - **Reviewer Pane**: テスト、レビュー

2.  **双方向通信 (Reactive Exchange)**:
    CLI を通じて、エージェントは他者のターミナルを操作・観察できます。
    - **Stimulus (Input)**: `forge send` でコマンドを送信
    - **Sensation (Observation)**: `forge read` で出力を確認

## インストール

**必須要件**:
- Python 3.10+
- tmux

```bash
# リポジトリをクローン
git clone https://github.com/your-org/agent-forge.git
cd agent-forge

# 開発モードでインストール
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 基本的な使い方

### 1. ワークスペースの初期化

カレントディレクトリに `.forge.yaml` 設定ファイルを生成します。

```bash
forge init
```

### 2. セッションの開始 (Departure)

定義された環境（tmux セッション）を立ち上げます。

```bash
forge start
```

### 3. エージェント間通信

別のターミナルから、稼働中のエージェント（ペイン）に対して指示を送ります。

```bash
# Implementer ペインに ls コマンドを実行させる
forge send implementer "ls -la"

# Implementer ペインの出力を確認する
forge read implementer
```

## 開発

```bash
# テストの実行
pytest
```

## ライセンス

MIT License
