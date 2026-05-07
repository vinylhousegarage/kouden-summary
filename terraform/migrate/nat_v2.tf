# AL2023 AMIを自動取得
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023*-x86_64"]
  }
}

# NATインスタンス (v2) の更新
resource "aws_instance" "nat_v2" {
  # 基本スペック
  ami           = data.aws_ami.al2023.id
  instance_type = "t2.micro"
  key_name      = "instance-key-002"

  # ネットワーク・セキュリティ設定
  subnet_id              = "subnet-0de9867b55c955be2"
  vpc_security_group_ids = ["sg-0cbab0718ed76d5db"]

  # NAT機能・権限設定
  source_dest_check    = false
  iam_instance_profile = "NAT-Instance-Role"

  # マスカレード（NAT）設定
  user_data = <<-EOT
    #!/bin/bash
    dnf install -y nftables
    echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/99-nat.conf
    sysctl -p /etc/sysctl.d/99-nat.conf
    systemctl enable --now nftables
    nft add table ip nat
    nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }
    nft add rule ip nat postrouting oifname "enX0" counter masquerade
    nft list ruleset > /etc/nftables/main.nft
  EOT

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
    volume_size = 8
    iops        = 3000
    throughput  = 125
  }

  # 管理タグ
  tags = {
    Name    = "nat-instance-v2"
    OS      = "AL2023"
    Version = "v2.1.0"
  }
}

# パブリックIP設定
resource "aws_eip" "nat_eip" {
  instance = aws_instance.nat_v2.id
  domain   = "vpc"
}
