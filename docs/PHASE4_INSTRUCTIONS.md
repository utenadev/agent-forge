# Phase 4: CLI の強化と品質向上 実装指示

Phase 3 までの実装で基本機能は整いました。続いて、Devinからのフィードバックに基づき、ツールの実用性と信頼性を高めるための強化を行います。

**目標:** `forge stop` コマンドの実装、エラーメッセージの改善、およびローカル E2E テストの作成。

**実装タスク:**

1.  **`forge stop` コマンドの実装 (`agent_forge/cli.py`, `agent_forge/session.py`):**
    *   **機能**: アクティブな Forge セッションを安全に終了（kill）する。
    *   **ロジック**:
        *   `agent_forge/session.py` に `stop_session(session_name: str)` 関数を追加。`libtmux` の `session.kill_session()` を使用。
        *   `cli.py` に `stop` コマンドを追加。引数でセッション名を指定可能にする（デフォルトは設定ファイルから）。
        *   セッションが存在しない場合は、エラーではなく「セッションは存在しません」と穏やかに終了する。

2.  **エラーハンドリングの改善 (`agent_forge/cli.py`):**
    *   現在 `sys.exit(1)` や `click.Abort()` で終了している部分を、より親切なメッセージに変更する。
    *   例: `send` コマンドでターゲットが見つからない場合:
        *   Before: `Error: Pane 'backend' not found in session.`
        *   After: `Error: Pane 'backend' not found. Available panes: [architect, implementer, reviewer]` (可能なら候補を表示)

3.  **ローカル E2E テストの作成 (`tests/e2e/test_live_tmux.py`):**
    *   **目的**: モックではなく、実際に `tmux` プロセスを立ち上げて動作確認を行う。
    *   **注意**: このテストは `pytest` のデフォルト実行からは除外するか、`@pytest.mark.e2e` などを付けて区別する（CI 環境に tmux がない場合があるため）。ただし、今回はローカル実行を前提とするため、まずは普通に書いて良い。
    *   **シナリオ**:
        1.  一時的な設定ファイルを作成。
        2.  `start_forge` でセッション起動。
        3.  `find_pane` でペイン取得。
        4.  `send_command` で "echo 'Hello E2E'" を送信。
        5.  `read_output` で出力を確認し、"Hello E2E" が含まれるか検証。
        6.  `stop_session` でクリーンアップ。

**テスト戦略:**
*   既存のユニットテスト (`tests/test_cli.py` 等) に `stop` コマンドのテストを追加（モック使用）。
*   `tests/e2e/` ディレクトリを新設し、実環境テストを配置。

**リファクタリング:**
*   `agent_forge/cli.py` が肥大化しつつあるため、エラーハンドリングや共通処理（セッション取得など）をヘルパー関数として整理することを検討してください。
