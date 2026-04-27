terraform {
  backend "s3" {
    bucket = "kouden-summary-tfstate"
    key    = "remove/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

# AWSプロバイダーの設定
provider "aws" {
  region = "ap-northeast-1"
}

# 関連セキュリティグループ
resource "aws_security_group" "flask_ec2_sg" {
  name        = "flask-ec2-sg"
  description = "Flask EC2 Security Group"
  vpc_id      = "vpc-09a84d9fab986d185"

  tags = {
    Name = "SG-EC2-Instance"
  }
}

# IAM インスタンスプロファイル
resource "aws_iam_instance_profile" "ecs_instance_role" {
  name = "ecsInstanceRole"
  role = "ecsInstanceRole"
}
