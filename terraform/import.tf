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
  id = "arn:aws:ecs:ap-northeast-1:626635405187:task-definition/flask-task:74"
}
