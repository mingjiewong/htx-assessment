# Application Load Balancer
resource "aws_lb" "app_alb" {
  name               = "htx-assessment-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = aws_subnet.public_subnet[*].id

  tags = {
    Name = "htx-assessment-alb"
  }
}

# Target Group for ALB
resource "aws_lb_target_group" "alb_tg" {
  name     = "htx-assessment-tg"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main_vpc.id

  health_check {
    healthy_threshold   = 5
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = "/"
    protocol            = "HTTP"
  }

  tags = {
    Name = "htx-assessment-tg"
  }
}

# ALB Listener (HTTPS)
resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.app_alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alb_tg.arn
  }
}

# Register EC2 Instance with ALB Target Group
resource "aws_lb_target_group_attachment" "ec2_alb_attachment" {
  count            = length(aws_instance.app_instance)
  target_group_arn = aws_lb_target_group.alb_tg.arn
  target_id        = aws_instance.app_instance[count.index].id
  port             = 3000
}