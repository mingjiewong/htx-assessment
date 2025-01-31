# ====================
# Terraform Variables
# ====================

# AWS Region where resources will be deployed
variable "region" {
  description = "AWS Region"
  type        = string
  default     = "ap-southeast-1"
}

# AMI ID for the EC2 instance
variable "ami_id" {
  description = "The AMI ID to use for the EC2 instance"
  type        = string
  default     = "ami-0198a868663199764" # Example: Ubuntu 22.04 LTS
}

# EC2 instance type
variable "ec2_instance_type" {
  description = "The EC2 instance type"
  type        = string
  default     = "t3.large"
}

# SSH key pair name for EC2 instance access
variable "ec2_ssh_key_name" {
  description = "SSH key pair name for EC2 instance"
  type        = string
}

# ARN of the SSL certificate for the Application Load Balancer (ALB)
variable "certificate_arn" {
  description = "The ARN of the SSL certificate for ALB"
  type        = string
}

# VPC CIDR Block
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# CIDR blocks for Public Subnets (one for each AZ)
variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets, one per AZ"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

# CIDR blocks for Private Subnets (one for each AZ)
variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets, one per AZ"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

# Availability Zones to deploy subnets
variable "availability_zones" {
  description = "List of Availability Zones for subnets"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b"]
}

# Hostname for the EC2 instance
variable "hostname" {
  description = "The hostname for the EC2 instance"
  type        = string
}

# IP address to allow SSH access to the EC2 instance
variable "personal_ip" {
  description = "The IP address to allow SSH access to the EC2 instance"
  type        = string
}

# Bastion Host AMI ID
variable "bastion_ami_id" {
  description = "The AMI ID to use for the Bastion Host"
  type        = string
  default     = "ami-08908d9e195550170" # Amazon Linux 2023 AMI
}