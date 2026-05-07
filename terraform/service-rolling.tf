# rolling update用ターゲットグループ
resource "aws_lb_target_group" "rolling_tg" {
  name        = "rolling-tg"
  port        = 5000
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = data.aws_vpc.main.id

  health_check {
    path                = "/health"
    port                = "5000"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# rolling update用サービス
resource "aws_ecs_service" "service_rolling" {
  name            = "service-rolling"
  cluster         = aws_ecs_cluster.main.arn
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = 1
  launch_type     = "EC2"

  deployment_controller {
    type = "ECS"
  }


  load_balancer {
    target_group_arn = aws_lb_target_group.rolling_tg.arn
    container_name   = "flask-web"
    container_port   = 5000
  }

  lifecycle {
    ignore_changes = [
      task_definition,
      load_balancer
    ]
  }
}

# rolling update用リスナー (HTTPS8000)
resource "aws_lb_listener" "rolling_test" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "8000"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = data.aws_acm_certificate.issued.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.rolling_tg.arn
  }
}

# セキュリティグループ（HTTPS8000）
resource "aws_vpc_security_group_ingress_rule" "alb_allow_8000" {
  security_group_id = "sg-080b3c56359547874"
  from_port         = 8000
  to_port           = 8000
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}
