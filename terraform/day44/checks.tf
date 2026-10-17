check "s3_public_access_block" {
  assert {
    condition = (
      aws_s3_bucket_public_access_block.secure.block_public_acls
      &&
      aws_s3_bucket_public_access_block.secure.ignore_public_acls
      &&
      aws_s3_bucket_public_access_block.secure.block_public_policy
      &&
      aws_s3_bucket_public_access_block.secure.restrict_public_buckets
    )

    error_message = "All S3 Block Public Access settings should be enabled."
  }
}
