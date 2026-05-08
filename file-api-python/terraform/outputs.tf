output "public_ip" {
  value = aws_instance.flask_server.public_ip
}

output "key_pair_name" {
  value       = aws_key_pair.deployer.key_name
  description = "SSH key pair name"
}

output "ssh_command" {
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.flask_server.public_ip}"
  description = "SSH command to connect to EC2"
}

output "api_url" {
  value       = "http://${aws_instance.flask_server.public_ip}:5000"
  description = "API URL"
}

output "instance_id" {
  value       = aws_instance.flask_server.id
  description = "EC2 Instance ID"
}