output "alb_public_url" {
  description = "Public URL for the Application Load Balancer"
  value       = "http://${aws_lb.app.dns_name}"
}
