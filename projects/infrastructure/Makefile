init:
	terraform init -backend-config=backend.hcl -reconfigure

plan_dev: init
	terraform plan   -var-file=vars/dev.tfvars

apply_dev: init
	terraform apply -var-file=vars/dev.tfvars -auto-approve

plan_prod: init
	terraform plan   -var-file=vars/prod.tfvars

apply_prod: init
	terraform apply -var-file=vars/prod.tfvars -auto-approve

destroy_dev: init
	terraform destroy -var-file=vars/dev.tfvars -auto-approve

destroy_prod: init
	terraform destroy -var-file=vars/prod.tfvars -auto-approve