# AL2NATインスタンス
resource "aws_instance" "nat_instance" {
  ami           = "ami-022282eb775c6a4fa"
  instance_type = "t2.micro"

  tags = {
    Name = "nat-instance"
  }
}

# 関連セキュリティグループ
resource "aws_security_group" "flask_nat_instance_sg" {
  name        = "flask-nat-instance-sg"
  description = "Allow private subnet instances to access the internet via NAT"
  vpc_id      = "vpc-09a84d9fab986d185"

  tags = {
    Name = "SG-NAT-Instance"
  }
}

# IAM インスタンスプロファイル
resource "aws_iam_instance_profile" "NAT_Instance_Role" {
  name = "NAT-Instance-Role"
  role = "NAT-Instance-Role"
}
