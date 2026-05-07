# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "sg-0e05e4fa1bba7a0a1"
resource "aws_security_group" "instance_v2_sg" {
  description = "Flask EC2 Security Group"
  egress = [{
    cidr_blocks      = []
    description      = "Allow Echo Request to NAT Instance"
    from_port        = 8
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "icmp"
    security_groups  = ["sg-0cbab0718ed76d5db"]
    self             = false
    to_port          = -1
    }, {
    cidr_blocks      = []
    description      = "Allow Ephemeral Ports for NAT Instance"
    from_port        = 1024
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-0cbab0718ed76d5db"]
    self             = false
    to_port          = 65535
    }, {
    cidr_blocks      = []
    description      = "Allow HTTP traffic to NAT Instance"
    from_port        = 80
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-0cbab0718ed76d5db"]
    self             = false
    to_port          = 80
    }, {
    cidr_blocks      = []
    description      = "Allow HTTPS traffic to NAT Instance"
    from_port        = 443
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-0cbab0718ed76d5db"]
    self             = false
    to_port          = 443
    }, {
    cidr_blocks      = []
    description      = "Allow traffic to RDS"
    from_port        = 3306
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-0af965b84d1192338"]
    self             = false
    to_port          = 3306
    }, {
    cidr_blocks      = []
    description      = "Allow traffic to VPC Endpoint"
    from_port        = 443
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-047202840ef4fc615"]
    self             = false
    to_port          = 443
    }, {
    cidr_blocks      = []
    description      = "Allow traffic to VPCE for S3"
    from_port        = 443
    ipv6_cidr_blocks = []
    prefix_list_ids  = ["pl-61a54008"]
    protocol         = "tcp"
    security_groups  = []
    self             = false
    to_port          = 443
  }]
  ingress = [{
    cidr_blocks      = []
    description      = "Allow Echo Request from NAT instance"
    from_port        = 8
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "icmp"
    security_groups  = ["sg-0cbab0718ed76d5db"]
    self             = false
    to_port          = -1
    }, {
    cidr_blocks      = []
    description      = "Allow SSH traffic from NAT instance"
    from_port        = 22
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-0cbab0718ed76d5db"]
    self             = false
    to_port          = 22
    }, {
    cidr_blocks      = []
    description      = "Allow traffic from ALB"
    from_port        = 5000
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = ["sg-080b3c56359547874"]
    self             = false
    to_port          = 5000
  }]
  name                   = "flask-ec2-sg"
  revoke_rules_on_delete = null
  tags = {
    Name = "SG-EC2-Instance"
  }
  tags_all = {
    Name = "SG-EC2-Instance"
  }
  vpc_id = "vpc-09a84d9fab986d185"
}
