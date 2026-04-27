# AL2023 AMIを自動取得
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023*-x86_64"]
  }
}

# NATインスタンス (v2) の作成
resource "aws_instance" "nat_v2" {
  # 基本スペック
  ami           = data.aws_ami.al2023.id
  instance_type = "t2.micro"
  key_name      = "instance-key-002"

  # ネットワーク・セキュリティ
  subnet_id              = "subnet-0de9867b55c955be2"
  vpc_security_group_ids = ["sg-0cbab0718ed76d5db"]
  source_dest_check      = false

  # 権限・セキュリティ設定
  iam_instance_profile = "NAT-Instance-Role"
  metadata_options {
    http_tokens   = "required"
    http_endpoint = "enabled"
  }

  # ストレージ
  root_block_device {
    volume_type = "gp3"
    volume_size = 8
    iops        = 3000
    throughput  = 125
  }

  # 管理タグ
  tags = {
    Name    = "nat-instance-v2"
    OS      = "AL2023"
    Version = "v2.0.0"
  }
}
