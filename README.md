## 香典集計（kouden summary app）

### 1. 概要
  - **目的**
    - 本アプリは、Ruby on Rails にて開発した香典集計アプリを Flask にて再構築したものです。
    - 処理の責務を明確にするため、軽量なフレームワークの Flask を採用しました。
    - 複雑なクエリを必要としないため、レスポンス性能に優れた MariaDB を採用しました。
    - インフラ全体の構成を柔軟に設計するため、クラウド基盤として AWS を採用しました。
    - 認証機能のセキュリティを強化するため、認証基盤として AWS Cognito を採用しました。
    - デプロイを自動化するため、CI/CDワークフロー として GitHub Actions を採用しました。

  - **対象ユーザー**
    - AWS Cognito による認証を受けたユーザー

  - **提供機能**
    - 認証機能（AWS Cognito）
    - 香典情報の表示・登録・編集・削除
    - 香典情報の集計表示
    - 香典情報の一括削除（初期状態へのリセット）

  - **前作からの変更点**
    - QRコード による投稿者招待機能は、セキュリティロジック簡素化のため除外しています。

### 2. 設計意図
  - **技術選定**
    - 既存の Ruby on Railsアプリ がアプリケーション層とデータベース層で構成されているため、AWS上 でもレイヤ分離を維持した構成としました。
    - アプリケーション層には、デバッグやトラブルシュートを容易にするため、インスタンスへの直接アクセスが可能な ECS（EC2起動タイプ）を採用しました。
    - データベースには、バックアップや可用性確保の運用負荷を軽減するため、RDS を採用しました。

  - **スケーラビリティ**
    - 負荷増加に対応可能な構成とするため、コンテナオーケストレーションとして ECS を採用しました。

  - **セキュリティ**
    - 認証基盤として、OAuth2.0 / OIDC に準拠した Cognito を採用しました。
    - JWT の署名およびクレーム検証を実装し、不正なリクエストを防止します。

  - **運用性**
    - デプロイを自動化するため、CI/CDワークフロー として GitHub Actions を採用しました。

  - **デプロイ構成**
    - CodeDeploy による Blue/Greenデプロイ を採用しました。
    - 本番切り替え前に新環境の正常性を確認します。

  - **機密情報管理**
    - 秘匿情報をセキュアに管理するため、SSM Parameter Store（SecureString）を採用しました。

  - **拡張性**
    - Fargate への移行で運用負荷の軽減が可能な設計としました。

### 3. アーキテクチャ設計
  - 本アプリは、設計意図で示した方針をもとに、以下の構成としています。

  - **AWS構成図**
    - [https://vinylhousegarage.github.io/kouden-summary/aws-diagram.svg](https://vinylhousegarage.github.io/kouden-summary/aws-diagram.svg)

  - **ALB**
    - 外部からのリクエストを受け付け、ECS へルーティング
    - リバースプロキシとして ECS の直接公開を回避し、ヘルスチェックで可用性を確保

  - **ECS（EC2起動タイプ）**
    - EC2インスタンス上 でコンテナを実行し、コンテナタスクを管理
    - EC2インスタンス への直接アクセスによるトラブルシュートに対応

  - **RDS（MariaDB）**
    - アプリケーションのデータを管理
    - マネージドサービスにより運用負荷を軽減

  - **ECR**
    - Dockerイメージの管理
    - CI/CDパイプライン と連携し、デプロイの一貫性を確保

  - **NAT（インスタンスタイプ）**
    - プライベートサブネット上の ECS から外部への通信に使用
    - インスタンスで構築し、コスト最適化と運用時のアクセス経路として活用

  - **Cognito**
    - ユーザー認証を担当
    - 認証機能を外部化し、セキュリティと実装コストを最適化

  - **SSM Parameter Store（SecureString）**
    - 環境変数・秘匿情報の管理
    - ソースコードから秘匿情報を分離し、安全性を確保

  - **GitHub Actions**
    - CI/CD を実行
    - デプロイの自動化により開発効率を向上

  - **Terraform**
    - Infrastructure as Code によるリソース管理
    - リソースを Terraform管理下 に置き、コードでリソースを構築

### 4. セキュリティ設計
  - **認証方式**
    - OAuth2.0 / OpenID Connect（OIDC）に準拠した Cognito をユーザーの認証に使用
    - 認証成功後、Cognito の リダイレクトURI に付与された code（認可コード）を用いて、トークン（id_token・access_token・refresh_token）を取得し、検証
    - トークンをデータベースに保存し、管理
    - ログアウト時、Cognito の logoutエンドポイント にリダイレクト

  - **セッション管理**
    - Flask-Session が自動でデータベースに sessionsテーブル を生成
    - 暗号化によるサイズの増加を考慮し、sessionsテーブル の dataカラム を mediumblob型 に変更
    - Fernet によって暗号化したトークンを dataカラム に格納
    - id_token から sub を抽出し、session_id に格納
    - ログアウト時、session_id とトークンを削除し、ログイン状態を無効化

  - **トークン検証**
    - Cognito の JSON Web Key Set（JWKs）を取得し Key ID を抽出
    - 抽出した Key ID と access_token の Key ID を照合し、一致する Key を PEM形式 の公開鍵に変換
    - 変換した公開鍵を用いて、リクエスト実行前に access_token の署名と標準クレーム（aud・iss・exp）を自動検証

  - **秘匿情報管理**
    - SSM Parameter Store のパラメータに、秘匿情報を SecureString として登録
    - ECSタスク定義 からパラメータを参照し、環境変数として設定
    - IAM ロールにより、パラメータへのアクセスを制御

### 5. データ構造
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

  - id_token の sub属性 を抽出し、session_idカラム に格納することで、ユーザーを識別しています。
  - 初回アクセス時、暗号化トークンの格納に備え、dataカラム は blob型 から mediumblob型 に変更されます。

### 6. システム構成
  - **技術スタック**
    - プログラミング言語：Python 3.12.12
    - フレームワーク：Flask 3.1.3
    - データベース：MariaDB 11.4.9
    - 仮想環境構築：Docker
      - 開発環境：Docker Compose で Dockerコンテナを起動
      - 本番環境：AWS ECS 上で Dockerコンテナを起動
    - テスト環境：GitHub Actions
    - ソースコードのローカルバージョン管理：Git
    - リモートリポジトリのホスティング：GitHub
    - CI/CD：GitHub Actions

  - **インフラ構成**
    - 開発環境サーバー：Werkzeug
    - 本番環境サーバー：Gunicorn
    - アプリのホスティング：AWS
      - コンテナ実行：ECS（EC2起動タイプ）
      - イメージ管理：ECR
      - データベース：RDS（MariaDB 11.4.9）
      - ロードバランサー：ALB
      - 秘匿情報管理：SSM Parameter Store（SecureString）
      - ドメイン・DNS管理：Route 53

### 7. アクセス情報
  - **GitHubリポジトリURL**
    - [https://github.com/vinylhousegarage/kouden-summary](https://github.com/vinylhousegarage/kouden-summary)
  - **アプリURL**
    - [https://kouden-summary.com](https://kouden-summary.com)

### 8. ライセンス
  - このプロジェクトは [MIT License](https://github.com/vinylhousegarage/kouden-summary/blob/main/LICENSE) のもとで公開されています。
