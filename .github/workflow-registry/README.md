# Workflow Registry

この workflow-registry/ に実行しないデプロイ方式のワークフローを退避させます。

| デプロイ方式 | workflows/ | workflow-registry/ |
| :--- | :--- | :--- |
| Rolling Update | app-deploy-rolling.yml | app-deploy-bg.yml |
| Blue/Green | app-deploy-bg.yml | app-deploy-rolling.yml |
