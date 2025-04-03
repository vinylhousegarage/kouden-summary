## 香典集計 ( kouden summary app )

### 1. 概要
  - **目的**
    - 本アプリは、Ruby on Rails で作成した「みんなで香典集計」を Flask で書き換えたものです。
    - FastAPI による API 分離を見据え、Flask で記述しています。
    - AWS Cognito を利用したログイン機能を導入し、セキュリティを強化しました。
    - GitHub Actions による CI/CD パイプラインを構築し、自動で AWS ECS にデプロイしています。

  - **範囲**
    - **対象ユーザー**
      - AWS Cognito で認証されたユーザー（ログインして香典情報を登録・編集・削除）
    - **提供機能**
      - ログイン機能（AWS Cognito）
      - 香典情報の登録・編集・削除
      - 集計画面の表示
      - サーバーサイドセッション管理

  - **前作からの変更点**
    - QRコードによる投稿者招待機能は、セキュリティロジック簡素化のため除外しています。

  - **URL**
    - **GitHubリポジトリ**
      - [https://github.com/vinylhousegarage/kouden-summary](https://github.com/vinylhousegarage/kouden-summary)
    - **AWSデプロイ**
      - [https://kouden-summary.com](https://kouden-summary.com)

### 2. セキュリティ設計
  - **認証方式：OAuth2.0 / OIDC準拠 + Cognito 実装**
    - OAuth2.0 / OpenID Connect（OIDC）に準拠した AWS Cognito を認証に使用
    - 認証成功後、Cognito から返される `authorization_code` を元にトークン（`id_token`, `access_token`, `refresh_token`）を取得し、検証
    - トークンはサーバー（Flask-Session + MariaDB）に保存し、管理
    - ログアウト時、Cognito の `logout` エンドポイントにリダイレクト

  - **セッション管理：Flask-Session + MariaDB + Fernet**
    - Flask-Session によりサーバーサイドセッションを実装
    - Fernet で暗号化したトークンをサーバーに格納
    - 暗号化によるサイズの増加を考慮し、セッションデータのカラムは `mediumBLOB` に変更
    - `id_token` の `sub` のみをセッションキーとして抽出し、管理
    - ログアウト時、セッションキーとトークンを削除し、ログイン状態を無効化

  - **トークン検証：`verify_cognito_jwt` 関数作成**
    - Cognito の JWKs を取得し、`kid` を抽出して公開鍵を作成
    - リクエスト実行前に、`access_token` の署名と標準クレーム（`aud`・`iss`・`exp`）を自動検証

  - **構成管理：AWS システムマネージャー**
    - envファイルに秘匿情報を置かず、AWS システムマネージャーに環境変数として登録
    - AWS IAM ロールの権限で、AWS システムマネージャーの環境変数を参照

  - **CD統合：GitHub Actions + ECS**
    - GitHub Actions で Dockerイメージを更新し、AWS ECR にプッシュ
    - 更新した Dockerイメージで、AWS ECS のタスク定義を更新

### 3. データ要件
  - **summaries テーブル（香典情報を管理）**

    | カラム名         | データ型        | 制約           | 説明                     |
    |------------------|-----------------|----------------|--------------------------|
    | id               | int(11)         | PRIMARY KEY    | 香典情報の一意な識別子   |
    | giver_name       | varchar(100)    | NOT NULL       | 氏名                     |
    | amount           | int(11)         | NOT NULL       | 金額                     |
    | address          | varchar(250)    | NULL 可        | 住所                     |
    | tel              | varchar(20)     | NULL 可        | 電話                     |
    | note             | varchar(250)    | NULL 可        | 備考                     |
    | user_cognito_id  | varchar(36)     | NOT NULL       | ユーザーの Cognito ID  |
    | created_at       | datetime        | NOT NULL       | 登録日時               |
    | updated_at       | datetime        | NOT NULL       | 更新日時               |

  - **sessions テーブル（Flask-Session による自動生成）**

    | カラム名   | データ型        | 制約           | 説明                           |
    |------------|-----------------|----------------|--------------------------------|
    | id         | int(11)         | PRIMARY KEY    | セッションの一意な識別子       |
    | session_id | varchar(255)    | UNIQUE         | ユーザーごとのセッションID     |
    | data       | blob            | NULL 可        | トークンデータ                |
    | expiry     | datetime        | NULL 可        | セッションの有効期限           |

  - **補足**
    - `sessions.data` カラムは初期状態では `blob` 型ですが、暗号化トークンの保存に備え、初回リクエスト時に `mediumblob` に自動でマイグレーションされます。

### 4. システム要件
  - **技術スタック**
    - プログラミング言語：Python 3.13.2
    - フレームワーク：Flask 3.1.0
    - データベース：MariaDB 11.4.4
    - 仮想環境構築：Docker
      - 開発環境：Docker Compose で Dockerコンテナを起動
      - 本番環境：AWS ECSタスクで Dockerコンテナを起動
    - テスト環境構築：GitHub Actions 上の runner で ruff を起動
    - ソースコードのローカルバージョン管理：Git
    - リモートリポジトリのホスティング：GitHub
    - CI/CD：GitHub Actions
      - CI：テスト
        - テスト：Ruff 0.11.2 によるリントチェックを実行
      - CD：ビルド / デプロイ
        - ビルド：Dockerイメージと AWS ECSタスク定義の更新
        - デプロイ：AWS ECSサービスで更新されたタスク定義を反映

  - **インフラ要件**
    - 開発環境サーバー：Werkzeug
    - 本番環境サーバー：Gunicorn
    - ネットワーク要件：AWS
      - アプリケーションホスティング：ECS EC2モード
      - ドメイン取得・DNS管理：Route 53
    - ドメイン：[https://kouden-summary.com](https://kouden-summary.com)

  - **開発環境**
    - OS：Windows 10
    - エディタ/IDE：Visual Studio Code
    - コンテナ開発環境：Docker Compose
    - バージョン管理の方法：
      - ブランチ戦略
        - mainブランチと作業ブランチに分けて管理
        - Pull Requestを通してmainブランチにマージ
        - 現在は個人開発であるため、コードレビューは任意で行うことが可能
      - コミットメッセージ規約
        - Conventional Commits (feature, refactor, docs などを使用)
