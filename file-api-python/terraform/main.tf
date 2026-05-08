resource "aws_key_pair" "deployer" {
  key_name   = var.key_name
  public_key = file("${path.module}/test_app.pub")
}

# IAM Role for S3 Access
resource "aws_iam_role" "ec2_s3_role" {
  name = "ec2-s3-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "s3-access-policy"
  role = aws_iam_role.ec2_s3_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ]
      Effect   = "Allow"
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-s3-profile"
  role = aws_iam_role.ec2_s3_role.name
}

resource "aws_security_group" "flask_sg" {
  name = "flask-security-group"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "flask_server" {
    ami                    = "ami-0eb38b817b93460ac"
    instance_type          = var.instance_type
    key_name               = aws_key_pair.deployer.key_name
    vpc_security_group_ids = [aws_security_group.flask_sg.id]
    iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
    
    user_data = base64encode(file("${path.module}/user_data.sh"))
}

