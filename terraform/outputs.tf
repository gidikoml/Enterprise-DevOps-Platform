output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "EKS API endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}

output "node_group_name" {
  description = "EKS managed node group name"
  value       = aws_eks_node_group.main.node_group_name
}