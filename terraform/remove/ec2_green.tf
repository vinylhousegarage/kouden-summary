# 1. AWSプロバイダーの設定
provider "aws" {
  region = "ap-northeast-1"
}

# 2. 停止中のEC2インスタンス (ec2-green-instance)
resource "aws_instance" "green_instance" {
  ami                         = "ami-0ed719a3283b1b8b6"
  instance_type               = "t2.micro"
  key_name                    = "instance-key-002"
  subnet_id                   = "subnet-0e0b9d18dc475ea54"
  vpc_security_group_ids      = ["sg-0e05e4fa1bba7a0a1"] # flask-ec2-sg
  iam_instance_profile        = aws_iam_instance_profile.ecs_instance_role.name
  associate_public_ip_address = false
  source_dest_check           = true

  root_block_device {
    volume_size = 30
    volume_type = "gp2"
    delete_on_termination = true
  }

  tags = {
    Name = "ec2-green-instance"
  }
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
