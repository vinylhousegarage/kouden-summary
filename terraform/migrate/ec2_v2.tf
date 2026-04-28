# AL2023ECS最適化AMI
data "aws_ami" "ecs_al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2023-ami-ecs-*-x86_64"]
  }
}

# EC2インスタンス (v2) の更新
resource "aws_instance" "ec2_v2" {
  # 基本スペック
  ami           = data.aws_ami.ecs_al2023.id
  instance_type = "t2.micro"
  key_name      = "instance-key-002"

  # ネットワーク・セキュリティ設定
  subnet_id              = "subnet-0e0b9d18dc475ea54"
  vpc_security_group_ids = ["sg-0e05e4fa1bba7a0a1"]

  # 権限設定
  iam_instance_profile = "ecsInstanceRole"

  # UserData
  user_data = <<-EOF
              #!/bin/bash
              echo ECS_CLUSTER=flask-cluster >> /etc/ecs/ecs.config
              EOF

  # 既存インスタンスを削除し新規作成
  user_data_replace_on_change = true

  # IMDSv2設定
  metadata_options {
    http_tokens   = "required"
    http_endpoint = "enabled"
  }

  # ストレージ設定
  root_block_device {
    volume_type = "gp3"
    volume_size = 30
    iops        = 3000
    throughput  = 125
  }

  # 管理タグ
  tags = {
    Name    = "ec2-instance-v2"
    OS      = "AL2023"
    Type    = "ECS-Optimized"
    Version = "2.0.0"
  }
}
