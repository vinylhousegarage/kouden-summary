# productionリスナー
data "aws_lb_listener" "production" {
  arn = var.alb_production_listener_arn
}

# testリスナー
data "aws_lb_listener" "test" {
  arn = var.alb_test_listener_arn
}

# 発行済みACM証明書
data "aws_acm_certificate" "issued" {
  domain   = "kouden-summary.com"
  statuses = ["ISSUED"]
}

