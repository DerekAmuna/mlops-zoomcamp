resource "aws_ecr_repository" "repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }
  force_delete = true
}

resource null_resource ecr_image {
   triggers = {
     python_file = md5(file(var.lambda_function_local_path))
     docker_file = md5(file(var.docker_image_local_path))
   }

   provisioner "local-exec" {
     command = <<EOF
             aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com
             docker build --platform linux/amd64 -t ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag} ..
             docker push ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag}
         EOF
   }
}

output "image_uri" {
  value = "${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag}"
  depends_on = [ null_resource.ecr_image ]
}

output "ecr_image_resource" {
  value = null_resource.ecr_image
}