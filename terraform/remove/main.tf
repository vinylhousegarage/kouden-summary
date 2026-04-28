# 1.State管理（S3）
terraform {
  backend "s3" {
    bucket = "kouden-summary-tfstate"
    key    = "remove/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

# 2.AWSプロバイダーの設定
provider "aws" {
  region = "ap-northeast-1"
}
