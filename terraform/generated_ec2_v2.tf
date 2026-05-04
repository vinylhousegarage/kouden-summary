# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform
resource "aws_lb" "alb" {
  client_keep_alive                           = 3600
  customer_owned_ipv4_pool                    = null
  desync_mitigation_mode                      = "defensive"
  dns_record_client_routing_policy            = null
  drop_invalid_header_fields                  = false
  enable_cross_zone_load_balancing            = true
  enable_deletion_protection                  = false
  enable_http2                                = true
  enable_tls_version_and_cipher_suite_headers = false
  enable_waf_fail_open                        = false
  enable_xff_client_port                      = false
  enable_zonal_shift                          = false
  idle_timeout                                = 60
  internal                                    = false
  ip_address_type                             = "ipv4"
  load_balancer_type                          = "application"
  name                                        = "flask-alb"
  preserve_host_header                        = false
  security_groups                             = ["sg-080b3c56359547874"]
  subnets                                     = ["subnet-028481d009085990d", "subnet-035ed6d9ceda38a7f"]
  tags                                        = {}
  tags_all                                    = {}
  xff_header_processing_mode                  = "append"
  access_logs {
    bucket  = ""
    enabled = false
    prefix  = null
  }
  connection_logs {
    bucket  = ""
    enabled = false
    prefix  = null
  }
}

# __generated__ by Terraform from "ecsInstanceRole"
resource "aws_iam_instance_profile" "al2_ec2_instance_role" {
  name     = "ecsInstanceRole"
  path     = "/"
  role     = "ecsInstanceRole"
  tags     = {}
  tags_all = {}
}

# __generated__ by Terraform
resource "aws_instance" "al2_ec2_instance" {
  ami                                  = "ami-0c6c393117fdd547a"
  associate_public_ip_address          = false
  availability_zone                    = "ap-northeast-1a"
  disable_api_stop                     = false
  disable_api_termination              = false
  ebs_optimized                        = false
  get_password_data                    = false
  hibernation                          = false
  iam_instance_profile                 = "ecsInstanceRole"
  instance_initiated_shutdown_behavior = "stop"
  instance_type                        = "t2.micro"
  monitoring                           = false
  placement_partition_number           = 0
  private_ip                           = "10.0.2.18"
  secondary_private_ips                = []
  security_groups                      = []
  source_dest_check                    = true
  subnet_id                            = "subnet-0e0b9d18dc475ea54"
  tags = {
    Name = "ec2-blue-instance"
  }
  tags_all = {
    Name = "ec2-blue-instance"
  }
  tenancy                     = "default"
  user_data = <<EOF
#!/bin/bash
echo ECS_CLUSTER=flask-cluster >> /etc/ecs/ecs.config;

yum install -y amazon-cloudwatch-agent

dd if=/dev/zero of=/swapfile bs=1M count=512
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
      },
      "disk": {
        "resources": ["/"],
        "measurement": ["disk_used_percent"]
      },
      "net": {
        "measurement": ["bytes_sent", "bytes_recv"]
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
    http_put_response_hop_limit = 1
    http_tokens                 = "optional"
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
    tags                  = {}
    tags_all              = {}
    volume_size           = 30
    volume_type           = "gp2"
  }
}

# CloudWatchエージェント用ポリシー
resource "aws_iam_role_policy_attachment" "cloudwatch_agent_server_policy" {
  role       = "ecsInstanceRole"
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# aws_ecs_cluster
resource "aws_ecs_cluster" "main" {
  name = "flask-cluster"
  tags = {}

  service_connect_defaults {
    namespace = "arn:aws:servicediscovery:ap-northeast-1:626635405187:namespace/ns-wncxecmrnmpeb5d4"
  }

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# aws_ecs_task_definition
resource "aws_ecs_task_definition" "main" {
  container_definitions = jsonencode(
    [
      {
        cpu = 128
        environment = [
          {
            name  = "DB_HOST"
            value = "flask-db-instance.cvy420ay6io1.ap-northeast-1.rds.amazonaws.com"
          },
          {
            name  = "LOG_LEVEL"
            value = "WARNING"
          },
          {
            name  = "MYSQL_DATABASE"
            value = "mariadb"
          },
        ]
        essential = true
        image     = "626635405187.dkr.ecr.ap-northeast-1.amazonaws.com/flask-repository:db5016345816c2a0425692b757e10b387015ae94"
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = "/ecs/flask-app"
            awslogs-region        = "ap-northeast-1"
            awslogs-stream-prefix = "ecs"
          }
        }
        memory            = 400
        memoryReservation = 256
        mountPoints       = []
        name              = "flask-web"
        portMappings = [
          {
            appProtocol   = "http"
            containerPort = 5000
            hostPort      = 5000
            name          = "flask-web-5000-tcp"
            protocol      = "tcp"
          },
        ]
        secrets = [
          {
            name      = "AWS_COGNITO_AUTHORITY"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_AUTHORITY"
          },
          {
            name      = "AWS_COGNITO_CLIENT_SECRET"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_CLIENT_SECRET"
          },
          {
            name      = "AWS_COGNITO_DOMAIN"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_DOMAIN"
          },
          {
            name      = "AWS_COGNITO_LOGOUT_URI"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_LOGOUT_URI"
          },
          {
            name      = "AWS_COGNITO_METADATA_URL"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_METADATA_URL"
          },
          {
            name      = "AWS_COGNITO_REDIRECT_URI"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_REDIRECT_URI"
          },
          {
            name      = "AWS_COGNITO_SCOPE"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_SCOPE"
          },
          {
            name      = "AWS_COGNITO_USER_POOL_CLIENT_ID"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_USER_POOL_CLIENT_ID"
          },
          {
            name      = "AWS_COGNITO_USER_POOL_ID"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_USER_POOL_ID"
          },
          {
            name      = "AWS_REGION"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_REGION"
          },
          {
            name      = "FERNET_KEY"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/FERNET_KEY"
          },
          {
            name      = "MYSQL_PASSWORD"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/MYSQL_PASSWORD"
          },
          {
            name      = "MYSQL_USER"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/MYSQL_USER"
          },
          {
            name      = "SECRET_KEY"
            valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/SECRET_KEY"
          },
        ]
        startTimeout   = 150
        stopTimeout    = 30
        systemControls = []
        volumesFrom    = []
      },
    ]
  )
  cpu                    = "128"
  enable_fault_injection = false
  execution_role_arn     = "arn:aws:iam::626635405187:role/ecsTaskExecutionRole"
  family                 = "flask-task"
  ipc_mode               = null
  memory                 = "400"
  network_mode           = "host"
  pid_mode               = null
  requires_compatibilities = [
    "EC2",
  ]
  skip_destroy  = false
  tags          = {}
  task_role_arn = "arn:aws:iam::626635405187:role/ecsTaskRole"
  track_latest  = false

  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
}
