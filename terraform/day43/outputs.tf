output "vpc_id" {
  description = "ID of the Terraform-managed VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the Terraform-managed VPC"
  value       = aws_vpc.main.cidr_block
}
