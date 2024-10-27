# Flask-Terraform AWS Resource Manager

This project is a Flask API designed to dynamically manage AWS resources (such as Lambda, S3, and RDS) using Terraform. It supports creating and deleting resources through REST endpoints and is designed for both local development with Docker Compose and Kubernetes deployments with Helm.

## Table of Contents

* Getting Started
* Project Structure
* Environment Variables
* Running Locally with Docker Compose
* Deploying on Kubernetes with Helm
* Endpoints


## Getting Started
### Prerequisites

* Docker and Docker Compose
* Kubernetes cluster (for deployment) and Helm
* AWS account and programmatic access setup (access key and secret key)

### Installation

    1. Clone the repository:

```bash
git clone https://github.com/ehud91/flask-terraform-aws-manager.git
cd flask-terraform-aws-manager
```
    2. Set up your AWS credentials as environment variables (see Environment Variables).

    3. Build and run the Docker containers with Docker Compose or deploy to Kubernetes using Helm.

### Project Structure    

```bash
flask-terraform-aws-manager/
│
├── resources.py             # Main Flask application
├── get_all_resources.py     # All methods for get all the created resouces from 
│                            # AWS - using Boto3 library
├── teraform_build_resources.py  # All methods for run terraform in order to 
│                            # build      resources in AWS
├── terraform/               # Terraform configurations for AWS resources
│   ├── main.tf              # Terraform file defining AWS resources
│   ├── variables.tf         # Terraform variables for AWS resources
│   └── ...                  # Other Terraform files
├── Dockerfile               # Dockerfile for Flask app and Terraform
├── docker-compose.yml       # Docker Compose file for local development
├── helm/                    # Helm chart for Kubernetes deployment
│   ├── templates/           # K8s templates (deployment, service, etc.)
│   └── values.yaml          # Default values for Helm deployment
└── README.md                # Project documentation
```

## Environment Variables

The following environment variables are required for the app to authenticate with AWS and interact with resources:

* AWS_ACCESS_KEY_ID: AWS access key ID
* AWS_SECRET_ACCESS_KEY: AWS secret access key
* AWS_DEFAULT_REGION: AWS region, e.g., us-east-1

These can be set directly in docker-compose.yml or values.yaml for Kubernetes.


### Running Locally with Docker Compose

    1. Build and Run the Containers:
```bash
docker-compose up --build
```

    2. Access the API: The API is available at http://localhost:5000.

    3. Available Endpoints:
        GET /resources: Get all AWS resources. 
        POST /resources: Creates AWS resources based on specified parameters.
        DELETE /resource: Deletes specified AWS resources.

Example Usage with curl
```bash
# Get resources
curl -X GET http://localhost:5000/resources \
    -H "Content-Type: application/json"

# Create resources
curl -X POST http://localhost:5000/resources \
    -H "Content-Type: application/json" \
    -d '{
          "bucket_name": "my-unique-bucket",
          "lambda_name": "my_lambda_function",
          "lambda_role_arn": "arn:aws:iam::123456789012:role/execution_role",
          "lambda_zip_file": "/path/to/lambda.zip",
          "db_name": "mydatabase",
          "db_username": "admin",
          "db_password": "password"
        }'

# Delete a resource
curl -X DELETE http://localhost:5000/resource \
    -H "Content-Type: application/json" \
    -d '{"resource_name": "my_lambda_function"}'
```

### Deploying on Kubernetes with Helm

To deploy this application on a Kubernetes cluster, you can use the provided Helm chart.

    1. Build and Push Docker Image: Make sure your Docker image is available in a container registry accessible to Kubernetes (e.g., Docker Hub, AWS ECR).
```bash
docker build -t flask-app .
docker push flask-app
```
    2. Update the Helm Values: Edit helm/flask-app/values.yaml to set the necessary environment variables, image repository, and tag.

    3. Deploy with Helm:
```bash
helm install flask-app helm/flask-app
```
    4. Accessing the API:

    * If using a LoadBalancer service type, obtain the external IP from kubectl get svc.
    * If using NodePort, access the service via <NodeIP>:<NodePort>.

### Endpoints
### POST /create-resources

Creates AWS resources based on the provided JSON parameters.

### Parameters (JSON):

    * bucket_name (string): Name of the S3 bucket.
    * lambda_name (string): Name of the Lambda function.
    * lambda_role_arn (string): ARN of the Lambda execution role.
    * lambda_zip_file (string): Path to the Lambda ZIP file.
    * db_name (string): Name of the RDS database.
    * db_username (string): Database username.
    * db_password (string): Database password.

Example Request:
```json
{
  "bucket_name": "my-unique-bucket",
  "lambda_name": "my_lambda_function",
  "lambda_role_arn": "arn:aws:iam::123456789012:role/execution_role",
  "lambda_zip_file": "/path/to/lambda.zip",
  "db_name": "mydatabase",
  "db_username": "admin",
  "db_password": "password"
}
```

### DELETE /delete-resource

Deletes a specific AWS resource.

### Parameters (JSON):

    resource_name (string): Name of the resource to delete.

Example Request:
```json
{
  "resource_name": "my_lambda_function"
}
```