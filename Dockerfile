# Base image with Python and Terraform installed
FROM hashicorp/terraform:1.0.11 as terraform

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Install Flask and Boto3
RUN pip3 install Flask boto3

# Copy application code
WORKDIR /app
COPY . .

# Expose Flask app port
EXPOSE 5000

# Run Flask app
CMD ["python3", "app.py"]