# 発行済みACM証明書
data "aws_acm_certificate" "issued" {
  domain   = "kouden-summary.com"
  statuses = ["ISSUED"]
}

# VPC
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["flask-vpc"]
  }
}
