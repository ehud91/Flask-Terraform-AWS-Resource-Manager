import os
import subprocess


# Define the directory containing your Terraform configurations
TERRAFORM_DIR = "./terraform"

def terraform_init():
    ### Initialize the Terraform configuration.
    subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR)

def terraform_apply(bucket_name, lambda_name, lambda_role_arn, lambda_zip_file, db_name, db_username, db_password):
    ### Apply Terraform configurations with specified variables.
    subprocess.run([
        "terraform", "apply", "-auto-approve",
        "-var", f"bucket_name={bucket_name}",
        "-var", f"lambda_name={lambda_name}",
        "-var", f"lambda_role_arn={lambda_role_arn}",
        "-var", f"lambda_zip_file={lambda_zip_file}",
        "-var", f"db_name={db_name}",
        "-var", f"db_username={db_username}",
        "-var", f"db_password={db_password}"
    ], cwd=TERRAFORM_DIR)

def terraform_destroy(resource_name):
    ### Destroy Terraform configurations for a specific resource.
    subprocess.run([
        "terraform", "destroy", "-auto-approve",
        "-var", f"resource_name={resource_name}"
    ], cwd=TERRAFORM_DIR)    

def terraform_output():
    ### Get output from Terraform.
    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True
    )
    return result.stdout

