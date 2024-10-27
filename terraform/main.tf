provider "aws" {
  region = "us-east-1"  # Set your preferred region
}

# S3 Bucket Resource
resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
}

# Lambda Function Resource
resource "aws_lambda_function" "lambda_function" {
  function_name = var.lambda_name
  runtime       = "python3.8"
  role          = var.lambda_role_arn
  handler       = "lambda_function.lambda_handler"
  filename      = var.lambda_zip_file

  environment {
    variables = {
      ENV = "production"
    }
  }
}

resource "aws_db_instance" "example_rds" {
  allocated_storage    = 20
  db_name              = var.db_name
  engine               = "postgres"
  engine_version       = "13.4"  # Use a supported PostgreSQL version, like 13.4
  instance_class       = "db.t2.micro"
  username             = var.db_username
  password             = var.db_password
  publicly_accessible  = true
  skip_final_snapshot  = true
  storage_type         = "gp2"  # General-purpose SSD
  backup_retention_period = 7   # Retain backups for 7 days
  multi_az             = false  # Set to true for high availability in a multi-AZ setup
}