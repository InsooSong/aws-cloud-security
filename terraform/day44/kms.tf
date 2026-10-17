resource "aws_kms_key" "s3" {
  description = "KMS key for Day 44 secure S3 bucket"

  enable_key_rotation = true

  tags = {
    Name = "day44-s3-key"
  }
}

resource "aws_kms_alias" "s3" {
  name          = "alias/day44-secure-s3"
  target_key_id = aws_kms_key.s3.key_id
}
