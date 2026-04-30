# ECSクラスター
import {
  to = aws_ecs_cluster.main
  id = "flask-cluster"
}

# ECSサービス
import {
  to = aws_ecs_service.main
  id = "flask-cluster/flask-service-rolling-update"
}

# ECSタスク定義
import {
  to = aws_ecs_task_definition.main
  id = "arn:aws:ecs:ap-northeast-1:626635405187:task-definition/flask-task:81"
}

# ALB
import {
  to = aws_lb.alb
  id = "arn:aws:elasticloadbalancing:ap-northeast-1:626635405187:loadbalancer/app/flask-alb/a038f59afa7e9191"
}

# ターゲットグループ
import {
  to = aws_lb_target_group.target_group_blue
  id = "arn:aws:elasticloadbalancing:ap-northeast-1:626635405187:targetgroup/flask-tg-blue/917f108766d09a04"
}

# AL2EC2インスタンス
import {
  to = aws_instance.al2_ec2_instance
  id = "i-0bef1c59761988c14"
}

# インスタンスプロファイル
import {
  to = aws_iam_instance_profile.al2_ec2_instance_role
  id = "ecsInstanceRole"
}
