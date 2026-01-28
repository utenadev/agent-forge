# Contributing to Agent Forge

Agent Forge への貢献に興味を持っていただきありがとうございます！

## 開発環境のセットアップ

このプロジェクトでは、パッケージ管理に `uv`、タスク管理に `Taskfile` (optional) を推奨しています。

### 1. 依存関係のインストール

```bash
# 仮想環境の作成と有効化
uv venv
source .venv/bin/activate

# 依存関係のインストール (テストツール含む)
uv pip install -e ".[dev]"
```

### 2. テストの実行

開発中は頻繁にテストを実行してください。

```bash
# 全テストの実行
pytest

# 特定のファイルのテスト
pytest tests/test_config.py
```

## コーディング規約

- **Python バージョン**: 3.10 以上をターゲットとしています。
- **スタイル**: 一般的な PEP 8 に準拠してください。
- **型ヒント**: 可能な限り型ヒント (`typing`) を記述してください。
- **テスト**: 新機能を追加する場合は、必ず対応するユニットテストを追加してください。TDD (Test Driven Development) を推奨します。

## プルリクエストのプロセス

1. このリポジトリをフォークします。
2. 機能追加やバグ修正のためのブランチを作成します (`git checkout -b feature/amazing-feature`)。
3. 変更をコミットします。
4. ブランチをプッシュします。
5. Pull Request を作成します。

## アーキテクチャ

詳細は `docs/FORGE_BLUEPRINT.md` および `docs/ARCHITECTURE.md` (作成中) を参照してください。
