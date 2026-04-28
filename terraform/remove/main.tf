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

# 3.AL2EC2Greenインスタンス（削除済）

# 4.関連セキュリティグループ（ec2-green-instance）
resource "aws_security_group" "flask_ec2_sg" {
  name        = "flask-ec2-sg"
  description = "Flask EC2 Security Group"
  vpc_id      = "vpc-09a84d9fab986d185"

  tags = {
    Name = "SG-EC2-Instance"
  }
}

# 5.IAM インスタンスプロファイル（ec2-instance）
resource "aws_iam_instance_profile" "ecs_instance_role" {
  name = "ecsInstanceRole"
  role = "ecsInstanceRole"
}

# 6.AL2NATインスタンス（削除済）

# 7.関連セキュリティグループ（nat-instance）
resource "aws_security_group" "flask_nat_instance_sg" {
  name        = "flask-nat-instance-sg"
  description = "Allow private subnet instances to access the internet via NAT"
  vpc_id      = "vpc-09a84d9fab986d185"

  tags = {
    Name = "SG-NAT-Instance"
  }
}

# 8.IAM インスタンスプロファイル（nat-instance）
resource "aws_iam_instance_profile" "NAT_Instance_Role" {
  name = "NAT-Instance-Role"
  role = "NAT-Instance-Role"
}
