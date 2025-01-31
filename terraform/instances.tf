# Bastion Host Instance
resource "aws_instance" "bastion" {
  count                       = length(aws_subnet.public_subnet)
  ami                         = var.bastion_ami_id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_subnet[count.index].id
  vpc_security_group_ids      = [aws_security_group.bastion_sg.id]
  key_name                    = var.ec2_ssh_key_name
  associate_public_ip_address = true

  tags = {
    Name = "htx-bastion-${count.index + 1}"
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
                sudo apt-get install -y git python3-pip

                ## From https://docs.docker.com/engine/install/ubuntu/#install-from-a-package
                # Add Docker's official GPG key:
                sudo apt-get update -y
                sudo apt-get install -y ca-certificates curl
                sudo install -m 0755 -d /etc/apt/keyrings
                sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
                sudo chmod a+r /etc/apt/keyrings/docker.asc

                # Add the repository to Apt sources:
                echo \
                  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
                  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
                  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                sudo apt-get update -y

                # Install Docker
                sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

                # Install Docker-Compose
                sudo apt install -y docker-compose
                ##

                # Pull and run Nginx container using Docker on port 3000
                sudo docker run -d --name nginx-server -p 3000:80 docker.io/library/nginx:latest

                # Clone the repository
                git clone https://github.com/mingjiewong/htx-assessment.git

                EOF

  depends_on = [
    aws_nat_gateway.nat_gateway_1,
    aws_nat_gateway.nat_gateway_2
  ]
}