# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform
resource "aws_instance" "ec2_v2" {
  ami                                  = "ami-07b6834a86f3632c8"
  associate_public_ip_address          = false
  availability_zone                    = "ap-northeast-1a"
  disable_api_stop                     = false
  disable_api_termination              = false
  ebs_optimized                        = false
  get_password_data                    = false
  hibernation                          = false
  iam_instance_profile                 = aws_iam_instance_profile.ecs_instance_profile.name
  instance_initiated_shutdown_behavior = "stop"
  instance_type                        = "t2.micro"
  key_name                             = "instance-key-002"
  monitoring                           = false
  placement_partition_number           = 0
  private_ip                           = "10.0.2.104"
  secondary_private_ips                = []
  security_groups                      = []
  source_dest_check                    = true
  subnet_id                            = "subnet-0e0b9d18dc475ea54"
  tags = {
    Name    = "ec2-instance-v2"
    OS      = "AL2023"
    Type    = "ECS-Optimized"
    Version = "2.0.0"
  }
  tags_all = {
    Name    = "ec2-instance-v2"
    OS      = "AL2023"
    Type    = "ECS-Optimized"
    Version = "2.0.0"
  }
  tenancy                     = "default"
  user_data = <<EOF
#!/bin/bash
echo ECS_CLUSTER=flask-cluster >> /etc/ecs/ecs.config;

yum install -y amazon-cloudwatch-agent

dd if=/dev/zero of=/swapfile bs=128M count=4
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab

cat << 'JSON' > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  "metrics": {
    "metrics_collected": {
      "mem": {
        "measurement": ["mem_used_percent", "mem_used", "mem_available"]
      },
      "swap": {
        "measurement": ["swap_used_percent"]
      }
    }
  }
}
JSON

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
EOF
  user_data_replace_on_change = true
  volume_tags                 = null
  vpc_security_group_ids      = ["sg-0e05e4fa1bba7a0a1"]
  capacity_reservation_specification {
    capacity_reservation_preference = "open"
  }
  credit_specification {
    cpu_credits = "standard"
  }
  enclave_options {
    enabled = false
  }
  lifecycle {
    ignore_changes = [
      user_data,
      user_data_replace_on_change,
    ]
  }
  maintenance_options {
    auto_recovery = "default"
  }
  metadata_options {
    http_endpoint               = "enabled"
    http_protocol_ipv6          = "disabled"
    http_put_response_hop_limit = 2
    http_tokens                 = "required"
    instance_metadata_tags      = "disabled"
  }
  private_dns_name_options {
    enable_resource_name_dns_a_record    = false
    enable_resource_name_dns_aaaa_record = false
    hostname_type                        = "ip-name"
  }
  root_block_device {
    delete_on_termination = true
    encrypted             = false
    iops                  = 3000
    tags                  = {}
    tags_all              = {}
    throughput            = 125
    volume_size           = 30
    volume_type           = "gp3"
  }
}
