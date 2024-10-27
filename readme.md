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

### Running Locally (Without Docker)

To run the Flask and Terraform application locally without using Docker, follow these steps:

1. Clone the Repository

    First, clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/flask-terraform-aws-manager.git
cd flask-terraform-aws-manager
```
3. Install Required Dependencies

    Next, install the necessary Python packages. Make sure you have pip installed, then run:
```bash
pip install -r requirements.txt
```
    Create a requirements.txt file in the project root with the following content if it doesn’t already exist:

4. Set Up AWS Credentials

    The application requires access to your AWS credentials to manage AWS resources. You can set these up using environment variables.
    Option 1: Set Credentials as Environment Variables

    Set the following environment variables in your terminal:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```
Replace your_access_key, your_secret_key, and us-east-1 with your actual AWS credentials and desired region.
Option 2: Use an AWS Configuration File

Alternatively, you can configure your AWS credentials using the AWS CLI. If you have the AWS CLI installed, you can run:

```bash
aws configure
```
Follow the prompts to enter your access key, secret key, region, and output format.

```bash
cd terraform
terraform init
cd ..
```
6. Run the Flask Application

Now, you can run the Flask application

```bash
python resources.py
```    
    The Flask API will start and be accessible at http://localhost:5000.
    


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
docker build -t your_dockerhub_username/flask-app .
docker push your_dockerhub_username/flask-app
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