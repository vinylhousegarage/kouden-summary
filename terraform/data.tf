# 443リスナー
data "aws_lb_listener" "443_listener" {
  arn = var.alb_443_listener_arn
}

# 4443リスナー
data "aws_lb_listener" "4443_listener" {
  arn = var.alb_4443_listener_arn
}
