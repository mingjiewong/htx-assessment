# Bastion Host Instance
resource "aws_instance" "bastion" {
  ami                         = var.bastion_ami_id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_subnet[0].id
  vpc_security_group_ids      = [aws_security_group.bastion_sg.id]
  key_name                    = var.ec2_ssh_key_name
  associate_public_ip_address = true

  tags = {
    Name = "htx-bastion"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y git
              EOF
}

# Application Instance
resource "aws_instance" "app_instance" {
  count                       = length(aws_subnet.private_subnet)
  ami                         = var.ami_id
  instance_type               = var.ec2_instance_type
  subnet_id                   = aws_subnet.private_subnet[count.index].id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  key_name                    = var.ec2_ssh_key_name
  associate_public_ip_address = false

  tags = {
    Name = "htx-assessment-ec2-${count.index + 1}"
  }

  user_data = <<-EOF
                #!/bin/bash

                # Update and install necessary packages
                sudo apt-get update -y
                sudo apt-get install -y podman git python3-pip

                # Install podman-compose
                sudo pip3 install podman-compose

                # Pull and run Nginx container using Podman on port 3000
                sudo podman run -d --name nginx-server -p 3000:80 docker.io/library/nginx:latest

                EOF

  depends_on = [aws_nat_gateway.nat_gateway]
}