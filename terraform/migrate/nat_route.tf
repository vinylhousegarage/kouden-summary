# ルートテーブル管理
resource "aws_route_table" "private_ecs" {
  vpc_id = "vpc-09a84d9fab986d185"

  tags = {
    Name = "RT-Private-ECS"
  }
}

# 0.0.0.0/0 のルート（nat-instance-v2へ向ける）
resource "aws_route" "private_nat_route" {
  route_table_id         = aws_route_table.private_ecs.id
  destination_cidr_block = "0.0.0.0/0"

  network_interface_id   = aws_instance.nat_v2.primary_network_interface_id
}

# サブネットとの関連付け（AZ:1a）
resource "aws_route_table_association" "private_a" {
  subnet_id      = "subnet-0e0b9d18dc475ea54"
  route_table_id = aws_route_table.private_ecs.id
}

# サブネットとの関連付け（AZ:1c）
resource "aws_route_table_association" "private_c" {
  subnet_id      = "subnet-0a18a0ee8bc6ef495"
  route_table_id = aws_route_table.private_ecs.id
}
