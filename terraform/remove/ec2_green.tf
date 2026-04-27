# 1. AWSプロバイダーの設定
provider "aws" {
  region = "ap-northeast-1"
}

# 3. セキュリティグループ (インスタンス用)
resource "aws_security_group" "flask_ec2_sg" {
  name        = "flask-ec2-sg"
  description = "Flask EC2 Security Group"
  vpc_id      = "vpc-09a84d9fab986d185"

  tags = {
    Name = "SG-EC2-Instance"
  }

  # インバウンド・アウトバウンドのルールは長くなるため
  # インポート後に terraform show で確認するのが効率的です
}

# 4. IAM インスタンスプロファイル
resource "aws_iam_instance_profile" "ecs_instance_role" {
  name = "ecsInstanceRole"
  role = "ecsInstanceRole"
}
