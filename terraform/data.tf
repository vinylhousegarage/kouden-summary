# productionリスナー
data "aws_lb_listener" "production" {
  arn = var.alb_production_listener_arn
}

# testリスナー
data "aws_lb_listener" "test" {
  arn = var.alb_test_listener_arn
}
