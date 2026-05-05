# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "arn:aws:elasticloadbalancing:ap-northeast-1:626635405187:listener/app/flask-alb/a038f59afa7e9191/981742d1002057f3"
resource "aws_lb_listener" "production" {
  alpn_policy                          = null
  certificate_arn                      = data.aws_acm_certificate.issued.arn
  load_balancer_arn                    = aws_lb.alb.arn
  port                                 = 443
  protocol                             = "HTTPS"
  routing_http_response_server_enabled = true
  ssl_policy                           = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  tags                                 = {}
  tags_all                             = {}
  default_action {
    order            = 1
    target_group_arn = aws_lb_target_group.blue_tg.arn
    type             = "forward"
    forward {
      stickiness {
        duration = 3600
        enabled  = false
      }
      target_group {
        arn    = aws_lb_target_group.blue_tg.arn
        weight = 100
      }
    }
  }
  mutual_authentication {
    ignore_client_certificate_expiry = false
    mode                             = "off"
    trust_store_arn                  = null
  }
  lifecycle {
    ignore_changes = [
      default_action,
    ]
  }
}

# __generated__ by Terraform from "arn:aws:elasticloadbalancing:ap-northeast-1:626635405187:listener/app/flask-alb/a038f59afa7e9191/1205685cc6087b64"
resource "aws_lb_listener" "test" {
  alpn_policy                          = null
  certificate_arn                      = data.aws_acm_certificate.issued.arn
  load_balancer_arn                    = aws_lb.alb.arn
  port                                 = 4443
  protocol                             = "HTTPS"
  routing_http_response_server_enabled = true
  ssl_policy                           = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  tags                                 = {}
  tags_all                             = {}
  default_action {
    order            = 1
    target_group_arn = aws_lb_target_group.green_tg.arn
    type             = "forward"
    forward {
      stickiness {
        duration = 3600
        enabled  = false
      }
      target_group {
        arn    = aws_lb_target_group.green_tg.arn
        weight = 1
      }
    }
  }
  mutual_authentication {
    ignore_client_certificate_expiry = false
    mode                             = "off"
    trust_store_arn                  = null
  }
  lifecycle {
    ignore_changes = [
      default_action,
    ]
  }
}

# __generated__ by Terraform from "arn:aws:elasticloadbalancing:ap-northeast-1:626635405187:listener/app/flask-alb/a038f59afa7e9191/3080ba7900a0ba7d"
resource "aws_lb_listener" "http_redirect" {
  alpn_policy                          = null
  certificate_arn                      = null
  load_balancer_arn                    = aws_lb.alb.arn
  port                                 = 80
  protocol                             = "HTTP"
  routing_http_response_server_enabled = true
  tags                                 = {}
  tags_all                             = {}
  default_action {
    order            = 1
    target_group_arn = null
    type             = "redirect"
    redirect {
      host        = "#{host}"
      path        = "/#{path}"
      port        = "443"
      protocol    = "HTTPS"
      query       = "#{query}"
      status_code = "HTTP_301"
    }
  }
}
