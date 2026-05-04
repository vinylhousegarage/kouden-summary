# CodeDeployアプリケーション
resource "aws_codedeploy_app" "codedeploy_app" {
  compute_platform = "ECS"
  name             = "codedeploy-app"
}

# Blue用ターゲットグループ
resource "aws_lb_target_group" "blue_tg" {
  name        = "blue-tg"
  port        = 5000
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path                = "/health"
    port                = "5000"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Green用ターゲットグループ
resource "aws_lb_target_group" "green_tg" {
  name        = "green-tg"
  port        = 5000
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path                = "/health"
    port                = "5000"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# productionリスナールール
resource "aws_lb_listener_rule" "production_rule" {
  listener_arn = data.aws_lb_listener.production.arn
  priority     = 2

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.blue_tg.arn
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }

  lifecycle {
    ignore_changes = [action]
  }
}

# testリスナールール
resource "aws_lb_listener_rule" "test_rule" {
  listener_arn = data.aws_lb_listener.test.arn
  priority     = 3

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.green_tg.arn
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }

  lifecycle {
    ignore_changes = [action]
  }
}

# CodeDeploy用ECSサービス
resource "aws_ecs_service" "service_codedeploy" {
  name            = "service-codedeploy"
  cluster         = var.ecs_cluster_arn
  task_definition = var.initial_task_definition_arn
  desired_count   = 1
  launch_type     = "EC2"

  deployment_controller {
    type = "CODE_DEPLOY"
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.blue_tg.arn
    container_name   = "flask-web"
    container_port   = 5000
  }

  depends_on = [aws_lb_listener_rule.production_rule]

  lifecycle {
    ignore_changes = [
      task_definition,
      load_balancer
    ]
  }
}

# CodeDeployデプロイグループ
resource "aws_codedeploy_deployment_group" "codedeploy_dg" {
  app_name               = aws_codedeploy_app.codedeploy_app.name
  deployment_config_name = "CodeDeployDefault.ECSAllAtOnce"
  deployment_group_name  = "codedeploy-dg"
  service_role_arn       = aws_iam_role.codedeploy.arn

  blue_green_deployment_config {
    deployment_ready_option {
      action_on_timeout = "CONTINUE_DEPLOYMENT"
    }
    terminate_blue_instances_on_deployment_success {
      action                           = "TERMINATE"
      termination_wait_time_in_minutes = 5
    }
  }

  deployment_style {
    deployment_option = "WITH_TRAFFIC_CONTROL"
    deployment_type   = "BLUE_GREEN"
  }

  ecs_service {
    cluster_name = var.ecs_cluster_name
    service_name = aws_ecs_service.service_codedeploy.name
  }

  load_balancer_info {
    target_group_pair_info {
      prod_traffic_route {
        listener_arns = [data.aws_lb_listener.production.arn]
      }
      test_traffic_route {
        listener_arns = [data.aws_lb_listener.test.arn]
      }
      target_group {
        name = aws_lb_target_group.blue_tg.name
      }
      target_group {
        name = aws_lb_target_group.green_tg.name
      }
    }
  }
}
