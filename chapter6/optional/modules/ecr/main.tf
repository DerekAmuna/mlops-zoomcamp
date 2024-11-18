resource "aws_ecr_repository" "model_repo" {
  name = var.ecr_model_repo_name
  image_tag_mutability = "MUTABLE"


  image_scanning_configuration {
    scan_on_push = false
  }
}


#### VIDEO COMMENTS ####
# 1. The image build-and-push step is typically handled by CI/CD pipeline rather than the IaC script
#However, the lambda configuration requires an existing Image URI in ECR to work
#  Therefore, they can upload a base image to bootstrap the lambda config, 
# which doesn't need to relate to the actual inference logic
# 2. The image_scanning_configuration is set to false to avoid unnecessary scans
# 3. The repository is set to mutable to allow for manual image tag updates

resource null_resource ecr_image {
  triggers = {
    python_file = md5(file(var.lambda_function_local_path))
    docker_file = md5(file(var.docker_file_local_path))
  }

  provisioner "local-exec" {
    command = <<EOF
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com
      aws ecr-public get-login-password --region eu-north-1 | docker login --username AWS --password-stdin public.ecr.aws
      docker build -t ${aws_ecr_repository.model_repo.repository_url}:${var.image_tag} .
      docker push ${aws_ecr_repository.model_repo.repository_url}:${var.image_tag} 
    EOF
  }
}

data aws_ecr_image lambda_image {
  depends_on = [
    null_resource.ecr_image
    ]
  repository_name = aws_ecr_repository.model_repo.name
  image_tag = var.image_tag
}

output "lambda_image_uri" {
  value = data.aws_ecr_image.lambda_image.image_uri
}
