output "vpc_id" {
  description = "ID of the secure VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_id" {
  description = "ID of the private subnet"
  value       = aws_subnet.private.id
}

output "security_group_id" {
  description = "ID of the internal security group"
  value       = aws_security_group.internal.id
}

output "s3_bucket_name" {
  description = "Name of the secure S3 bucket"
  value       = aws_s3_bucket.secure.id
}

output "kms_key_arn" {
  description = "ARN of the KMS key used for S3 encryption"
  value       = aws_kms_key.s3.arn
}

output "s3_reader_role_arn" {
  description = "ARN of the least-privilege S3 reader role"
  value       = aws_iam_role.s3_reader.arn
}
