resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "day44-secure-vpc"
  }
}

resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id

  cidr_block = var.private_subnet_cidr

  map_public_ip_on_launch = false

  tags = {
    Name = "day44-private-subnet"
  }
}

resource "aws_security_group" "internal" {
  name        = "day44-internal-sg"
  description = "Allow internal HTTPS traffic only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS from inside the VPC"

    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    cidr_blocks = [
      var.vpc_cidr
    ]
  }

  egress {
    description = "Allow outbound traffic"

    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Name = "day44-internal-sg"
  }
}
