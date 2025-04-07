## 香典集計 ( kouden summary app )

### 1. 概要
  - **目的**
    - 本アプリは、Ruby on Rails にて開発した香典集計アプリを Flask によって再構築したものです。
    - FastAPI を用いた認証機能の API化 を見据え、フレームワークを Flask に変更しました。
    - AWS Cognito を導入した認証機能により、セキュリティを強化しています。
    - GitHub Actions による CI/CDワークフロー を実装し、自動で AWS ECS にデプロイします。

  - **対象ユーザー**
    - AWS Cognito による認証を受けたユーザー

  - **提供機能**
    - 認証機能 ( AWS Cognito )
    - 香典情報の表示・登録・編集・削除
    - 香典情報の集計表示
    - 香典情報の一括削除 ( 初期状態へのリセット )

  - **前作からの変更点**
    - QRコード による投稿者招待機能は、セキュリティロジック簡素化のため除外しています。

### 2. セキュリティ設計
  - **認証方式**
    - OAuth2.0 / OpenID Connect ( OIDC ) に準拠した AWS Cognito をユーザーの認証に使用
    - 認証成功後、Cognito のリダイレクトURIに付与された code ( 認可コード ) を用いて、トークン ( id_token ・ access_token ・ refresh_token ) を取得し、検証
    - トークンをデータベースに保存し、管理
    - ログアウト時、Cognito の logoutエンドポイント にリダイレクト

  - **セッション管理**
    - Flask-Session が自動でデータベースに sessionsテーブル を生成
    - 暗号化によるサイズの増加を考慮し、sessionsテーブル の dataカラム を mediumblob型 に変更
    - Fernet によって暗号化したトークンを dataカラム に格納
    - id_token から sub を抽出し、session_id に格納
    - ログアウト時、session_id とトークンを削除し、ログイン状態を無効化

  - **トークン検証**
    - Cognito の JSON Web Key Set ( JWKs ) を取得し Key ID を抽出
    - 抽出した Key ID と access_token の Key ID を照合し、一致する Key を PEM形式 の公開鍵に変換
    - 変換した公開鍵を用いて、リクエスト実行前に access_token の署名と標準クレーム ( aud ・ iss ・ exp ) を自動検証

  - **秘匿情報管理**
    - 秘匿情報を AWS SSM ( パラメータストア ) にて、パラメータとして登録
    - AWS ECS タスク定義にてパラメータを参照し、環境変数として設定
    - AWS IAM ロールの権限により、環境変数を取得

  - **CI/CD構成**
    - GitHub Actions による CI/CDワークフロー を実装、テスト・ビルド・デプロイを自動化
    - ruff によるリントチェックを実行し、構文やスタイルを検証
    - Dockerイメージ をビルドし、AWS ECR にプッシュ
    - ビルドした Dockerイメージ で AWS ECS のタスク定義を更新し、デプロイ

### 3. データ構造
  - **summaries テーブル**

    | カラム名         | データ型        | 制約                              | 初期値              | 説明                               |
    |------------------|-----------------|-----------------------------------|---------------------|------------------------------------|
    | id               | int(11)         | PRIMARY KEY, auto_increment       | NULL                | 香典情報の一意な識別子             |
    | giver_name       | varchar(100)    | NOT NULL                          | NULL                | 氏名                               |
    | amount           | int(11)         | NOT NULL                          | NULL                | 金額                               |
    | address          | varchar(250)    | NULLABLE                          | NULL                | 住所                               |
    | tel              | varchar(20)     | NULLABLE                          | NULL                | 電話                               |
    | note             | varchar(250)    | NULLABLE                          | NULL                | 備考                               |
    | user_cognito_id  | varchar(36)     | NOT NULL                          | NULL                | ユーザー識別ID   |
    | created_at       | datetime        | NOT NULL                          | current_timestamp() | 登録日時                           |
    | updated_at       | datetime        | NOT NULL                          | current_timestamp() | 更新日時                           |

  - **sessions テーブル**

    | カラム名   | データ型        | 制約                              | 初期値 | 説明                           |
    |------------|-----------------|-----------------------------------|--------|--------------------------------|
    | id         | int(11)         | PRIMARY KEY, auto_increment       | NULL   | session の一意な識別子       |
    | session_id | varchar(255)    | UNIQUE                            | NULL   |  id_token から抽出した sub     |
    | data       | blob            | NULLABLE                          | NULL   | 暗号化されたトークン           |
    | expiry     | datetime        | NULLABLE                          | NULL   | session の有効期限           |

  - id_token の sub属性を抽出し、session_idカラム に格納することで、ユーザーを識別しています。
  - 初回アクセス時、暗号化トークンの格納に備え、dataカラム は blob型 から mediumblob型 に変更されます。

### 4. システム構成
  - **技術スタック**
    - プログラミング言語：Python 3.13.2
    - フレームワーク：Flask 3.1.0
    - データベース：MariaDB 11.4.4
    - 仮想環境構築：Docker
      - 開発環境：Docker Compose で Dockerコンテナを起動
      - 本番環境：AWS ECS 上で Dockerコンテナを起動
    - テスト環境：GitHub Actions
    - ソースコードのローカルバージョン管理：Git
    - リモートリポジトリのホスティング：GitHub
      - URL：[https://github.com/vinylhousegarage/kouden-summary](https://github.com/vinylhousegarage/kouden-summary)
    - CI/CD：GitHub Actions

  - **インフラ構成**
    - 開発環境サーバー：Werkzeug
    - 本番環境サーバー：Gunicorn
    - クラウドサービス：AWS
      - アプリケーションホスティング：ECS ( EC2モード )
      - ロードバランサー：ALB
      - データベース：RDS ( MariaDB 11.4.4 )
      - イメージレジストリ：ECR
      - 構成管理：SSM ( パラメータストア )
      - ドメイン・DNS管理：Route 53
    - アプリ公開URL：[https://kouden-summary.com](https://kouden-summary.com)

### 5. ライセンス
  - このプロジェクトは [MIT License](https://github.com/vinylhousegarage/kouden-summary/blob/main/LICENSE) のもとで公開されています。
