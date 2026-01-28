# Forge Resources: References & Inspirations

ユーザーより提供された、tmux を活用した AI エージェント連携および環境構築に関するリソース集です。
`agent-forge` の設計・実装において、これらの知見をベースにします。

## 1. Tmux + AI Agent Collaboration
AI エージェントを tmux ペインで並列稼働させ、連携させる手法について。

*   **tmux + Claude Codeで実現する並列開発 - 組織での活用方法とベストプラクティス**
    *   [Qiita Link](https://qiita.com/pythonista0328/items/409defd8f06f506728aa)
    *   *Key Takeaway*: 役割分担、並列実行による生産性向上。

*   **私が始めたAI協働生活 〜失敗から学んだ仕様駆動とサブエージェント連携〜**
    *   [Qiita Link](https://qiita.com/sasakiy0819/items/4297b6db6ad2057fe5cf)
    *   *Key Takeaway*: 仕様駆動開発 (SDD)、サブエージェントへのタスク委譲。

*   **Claude Codeを並列組織化してClaude Code "Company"にするtmuxコマンド集**
    *   [Zenn Link](https://zenn.dev/kazuph/articles/beb87d102bd4f5)
    *   *Key Takeaway*: コマンド集によるオペレーションの効率化。

*   **現実的なAI並列実装**
    *   [Zenn Link](https://zenn.dev/fatricepaddyy/articles/parallel-implementation#tmux%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    *   *Key Takeaway*: 実用的な運用フロー。

## 2. Environment Automation (Shogun Style)
tmux 環境構築の自動化について。

*   **Multi-Agent Shogun (Reference Implementation)**
    *   [GitHub Link](https://github.com/yohey-w/multi-agent-shogun/blob/main/shutsujin_departure.sh#L291)
    *   *Key Takeaway*: `shutsujin_departure.sh` による「出陣」メタファー。環境変数注入、画面分割の一括実行。

*   **【shell】tmuxの作業画面を一発で構築するコマンドを作ってみた**
    *   [DevelopersIO Link](https://dev.classmethod.jp/articles/tmux_create_devenv_display/)

*   **smug (Session Manager)**
    *   [GitHub Link](https://github.com/ivaaaan/smug)
    *   *Key Takeaway*: 設定ファイルによるセッション管理（tmuxp の Go 版のようなツール）。

## 3. Core Technologies
`agent-forge` が採用する技術スタック。

*   **tmuxp**
    *   [GitHub](https://github.com/tmux-python/tmuxp) | [Docs](https://tmuxp.git-pull.com/index.html)
    *   *Role*: YAML/JSON による宣言的なセッション構成管理。`libtmux` のラッパー。

*   **libtmux**
    *   [GitHub](https://github.com/tmux-python/libtmux)
    *   *Role*: Python から tmux を操作するための強力な API (send-keys, capture-pane 等)。
