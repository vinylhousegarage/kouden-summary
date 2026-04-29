# 動作環境の固定
terraform {
  required_version = "~> 1.14"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# 接続先の設定
provider "aws" {
  region = "ap-northeast-1"
}
