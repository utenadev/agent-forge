# 実装計画: Agent Forge

この計画は `agent-forge` CLI ツールの構築手順を概説します。

## Phase 1: スケルトンと CLI 基盤
**目標:** プロジェクト構造を確立し、基本的な CLI エントリーポイントを作成する。

- [x] **プロジェクトセットアップ:**
    - `pyproject.toml` の依存関係を確認する (`tmuxp`, `libtmux`, CLI用の `click` または `typer`)。
    - `agent_forge/__init__.py` がバージョンを公開しているか確認する。
- [x] **CLI エントリーポイント (`agent_forge/cli.py`):**
    - `click` を使用して基本的なコマンド構造を実装する。
    - コマンドを定義する: `init`, `start`, `send`, `read`, `list`。
    - ロギング設定をセットアップする。

## Phase 2: Forge ジェネレーター (設定)
**目標:** 宣言的な環境ファイル (`.forge.yaml`) を生成・管理する。

- [x] **テンプレートエンジン:**
    - `.forge.yaml` 用のデフォルトテンプレートを作成する (標準的な3ペインレイアウト)。
    - `forge init` を実装する:
        - 既存の設定を確認する。
        - 存在しない場合、デフォルト設定を書き込む。
- [x] **Config ローダー:**
    - `.forge.yaml` を読み込むユーティリティを実装する (`tmuxp.config` のラッパー)。

## Phase 3: コントローラー (ランタイム)
**目標:** `libtmux` を介して tmux セッションを制御するコアロジックを実装する。

- [x] **セッションマネージャー (`agent_forge/session.py`):**
    - `start_forge(config_path)`: `tmuxp` を使用してセッションをロードする。
    - `find_pane(session, name)`: 名前またはインデックスでペインを特定するヘルパー。
- [x] **通信プリミティブ (`agent_forge/actions.py`):**
    - `send_command(pane, cmd)`: `send-keys` の実装。
    - `read_output(pane, lines=100)`: `capture-pane` の実装。
    - `broadcast(session, cmd)`: すべてのペインにコマンドを送信する (未実装/YAGNI)。

## Phase 4: CLI の強化と品質向上 (Devin Feedback)
**目標:** ツールの堅牢性とユーザビリティを向上させる。

- [ ] **`forge stop` の実装:**
    - 指定したセッション（デフォルトは設定ファイルの定義）を終了するコマンド。
    - 終了時にペインのログを保存するオプション (`--archive`) を検討。
- [ ] **エラーハンドリングの改善:**
    - セッションが見つからない、ペイン名が曖昧などのエラー時に、具体的な解決策を提示するメッセージを表示する。
    - Python のトレースバックを直接表示せず、ユーザーフレンドリーなエラーにする。
- [ ] **ローカル E2E テスト:**
    - 実際に tmux セッションを立ち上げ、`send` と `read` が機能することを確認するスクリプト (`tests/e2e/`) を作成する。
    - モックだけでは検証できない `libtmux` のバージョン互換性などを担保する。

## Phase 5: エージェント活用ガイド (Prompt Engineering)
**目標:** AI エージェントがツールを効果的に使用できるようにする (MCPサーバー化は保留)。

- [ ] **エージェント向けマニュアル (`docs/FORGE_MANUAL.md`):**
    - AI エージェント（Claude, Gemini）が `forge` コマンドの使い方を学習するためのドキュメント。
- [ ] **システムプロンプトテンプレート:**
    - 各役割（Architect, Implementer）向けのシステムプロンプト例を作成する。
    - "あなたは Architect です。Implementer ペインに対して `forge send` で指示を出してください" などのインストラクション。

## Phase 6: 機能拡張 (Future)
**目標:** さらなる機能追加。

- [ ] **`forge list` の詳細化:**
    - 各ペインで実行中のプロセス名や、最終更新時間を表示する。
- [ ] **ワークスペースの多様化:**
    - `forge init --template mob-programming` など、複数のテンプレートに対応する。
