# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "flask-cluster"
resource "aws_ecs_cluster" "main" {
  name     = "flask-cluster"
  tags     = {}
  tags_all = {}
  service_connect_defaults {
    namespace = "arn:aws:servicediscovery:ap-northeast-1:626635405187:namespace/ns-wncxecmrnmpeb5d4"
  }
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

# __generated__ by Terraform from "flask-cluster/flask-service-rolling-update"
resource "aws_ecs_service" "main" {
  availability_zone_rebalancing      = "DISABLED"
  cluster                            = "arn:aws:ecs:ap-northeast-1:626635405187:cluster/flask-cluster"
  deployment_maximum_percent         = 100
  deployment_minimum_healthy_percent = 0
  desired_count                      = 1
  enable_ecs_managed_tags            = true
  enable_execute_command             = false
  force_delete                       = null
  force_new_deployment               = null
  health_check_grace_period_seconds  = 30
  iam_role                           = "/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS"
  launch_type                        = "EC2"
  name                               = "flask-service-rolling-update"
  propagate_tags                     = "NONE"
  scheduling_strategy                = "REPLICA"
  tags                               = {}
  tags_all                           = {}
  task_definition                    = "flask-task:74"
  triggers                           = {}
  wait_for_steady_state              = null
  alarms {
    alarm_names = []
    enable      = false
    rollback    = false
  }
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  deployment_controller {
    type = "ECS"
  }
  load_balancer {
    container_name   = "flask-web"
    container_port   = 5000
    elb_name         = null
    target_group_arn = "arn:aws:elasticloadbalancing:ap-northeast-1:626635405187:targetgroup/flask-tg-blue/917f108766d09a04"
  }
  ordered_placement_strategy {
    field = "memory"
    type  = "binpack"
  }
}

# __generated__ by Terraform from "arn:aws:ecs:ap-northeast-1:626635405187:task-definition/flask-task:74"
resource "aws_ecs_task_definition" "main" {
  container_definitions = jsonencode([{
    cpu = 512
    environment = [{
      name  = "DB_HOST"
      value = "flask-db-instance.cvy420ay6io1.ap-northeast-1.rds.amazonaws.com"
      }, {
      name  = "LOG_LEVEL"
      value = "WARNING"
      }, {
      name  = "MYSQL_DATABASE"
      value = "mariadb"
    }]
    essential = true
    #healthCheck = {
    #  command     = ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]
    #  interval    = 30
    #  retries     = 5
    #  startPeriod = 30
    #  timeout     = 10
    #}
    image = "626635405187.dkr.ecr.ap-northeast-1.amazonaws.com/flask-repository:db5016345816c2a0425692b757e10b387015ae94"
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/flask-app"
        awslogs-region        = "ap-northeast-1"
        awslogs-stream-prefix = "ecs"
      }
    }
    memory            = 512
    memoryReservation = 307
    mountPoints       = []
    name              = "flask-web"
    portMappings = [{
      appProtocol   = "http"
      containerPort = 5000
      hostPort      = 5000
      name          = "flask-web-5000-tcp"
      protocol      = "tcp"
    }]
    secrets = [{
      name      = "AWS_COGNITO_AUTHORITY"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_AUTHORITY"
      }, {
      name      = "AWS_COGNITO_CLIENT_SECRET"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_CLIENT_SECRET"
      }, {
      name      = "AWS_COGNITO_DOMAIN"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_DOMAIN"
      }, {
      name      = "AWS_COGNITO_LOGOUT_URI"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_LOGOUT_URI"
      }, {
      name      = "AWS_COGNITO_METADATA_URL"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_METADATA_URL"
      }, {
      name      = "AWS_COGNITO_REDIRECT_URI"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_REDIRECT_URI"
      }, {
      name      = "AWS_COGNITO_SCOPE"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_SCOPE"
      }, {
      name      = "AWS_COGNITO_USER_POOL_CLIENT_ID"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_USER_POOL_CLIENT_ID"
      }, {
      name      = "AWS_COGNITO_USER_POOL_ID"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_COGNITO_USER_POOL_ID"
      }, {
      name      = "AWS_REGION"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/AWS_REGION"
      }, {
      name      = "FERNET_KEY"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/FERNET_KEY"
      }, {
      name      = "MYSQL_PASSWORD"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/MYSQL_PASSWORD"
      }, {
      name      = "MYSQL_USER"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/MYSQL_USER"
      }, {
      name      = "SECRET_KEY"
      valueFrom = "arn:aws:ssm:ap-northeast-1:626635405187:parameter/param-store/SECRET_KEY"
    }]
    startTimeout   = 150
    stopTimeout    = 30
    systemControls = []
    volumesFrom    = []
  }])
  cpu                      = "512"
  enable_fault_injection   = false
  execution_role_arn       = "arn:aws:iam::626635405187:role/ecsTaskExecutionRole"
  family                   = "flask-task"
  ipc_mode                 = null
  memory                   = "512"
  network_mode             = "host"
  pid_mode                 = null
  requires_compatibilities = ["EC2"]
  skip_destroy             = null
  tags                     = {}
  tags_all                 = {}
  task_role_arn            = "arn:aws:iam::626635405187:role/ecsTaskRole"
  track_latest             = false
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
}
