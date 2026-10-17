data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type = "Service"

      identifiers = [
        "ec2.amazonaws.com"
      ]
    }

    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role" "s3_reader" {
  name = "day44-secure-s3-reader"

  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

data "aws_iam_policy_document" "s3_read" {
  statement {
    sid    = "ReadSecureBucket"
    effect = "Allow"

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.secure.arn}/*"
    ]
  }

  statement {
    sid    = "DecryptSecureBucketObjects"
    effect = "Allow"

    actions = [
      "kms:Decrypt"
    ]

    resources = [
      aws_kms_key.s3.arn
    ]
  }
}

resource "aws_iam_policy" "s3_read" {
  name        = "day44-secure-s3-read"
  description = "Least-privilege read access to the Day 44 secure bucket"

  policy = data.aws_iam_policy_document.s3_read.json
}

resource "aws_iam_role_policy_attachment" "s3_read" {
  role       = aws_iam_role.s3_reader.name
  policy_arn = aws_iam_policy.s3_read.arn
}
