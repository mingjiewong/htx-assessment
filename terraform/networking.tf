# VPC Setup
resource "aws_vpc" "main_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "htx-assessment-vpc"
  }
}

# Internet Gateway for VPC
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "htx-assessment-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  map_public_ip_on_launch = true
  availability_zone       = var.availability_zones[count.index]

  tags = {
    Name = "htx-assessment-public-subnet-${count.index + 1}"
  }
}

# Private Subnet
resource "aws_subnet" "private_subnet" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "htx-assessment-private-subnet-${count.index + 1}"
  }
}

# Allocate Elastic IPs for NAT Gateways
resource "aws_eip" "nat_eip_1" {}

resource "aws_eip" "nat_eip_2" {}

# Create NAT Gateway in first Public Subnet
resource "aws_nat_gateway" "nat_gateway_1" {
  allocation_id = aws_eip.nat_eip_1.id
  subnet_id     = aws_subnet.public_subnet[0].id

  tags = {
    Name = "htx-nat-gateway-1"
  }

  depends_on = [aws_internet_gateway.igw]
}

# Create NAT Gateway in second Public Subnet
resource "aws_nat_gateway" "nat_gateway_2" {
  allocation_id = aws_eip.nat_eip_2.id
  subnet_id     = aws_subnet.public_subnet[1].id

  tags = {
    Name = "htx-nat-gateway-2"
  }

  depends_on = [aws_internet_gateway.igw]
}

# Route Table for Public Subnet
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "htx-assessment-public-rt"
  }
}

# Associate Route Tables with Public Subnets
resource "aws_route_table_association" "public_assoc" {
  count          = length(aws_subnet.public_subnet)
  subnet_id      = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.public_rt.id
}

# Create Route Table for the first Private Subnet
resource "aws_route_table" "private_rt_1" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_1.id
  }

  tags = {
    Name = "htx-private-rt-1"
  }
}

# Create Route Table for the second Private Subnet
resource "aws_route_table" "private_rt_2" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_2.id
  }

  tags = {
    Name = "htx-private-rt-2"
  }
}

# Associate Route Table with the first Private Subnet
resource "aws_route_table_association" "private_assoc_1" {
  subnet_id      = aws_subnet.private_subnet[0].id
  route_table_id = aws_route_table.private_rt_1.id
}

# Associate Route Table with the second Private Subnet
resource "aws_route_table_association" "private_assoc_2" {
  subnet_id      = aws_subnet.private_subnet[1].id
  route_table_id = aws_route_table.private_rt_2.id
}