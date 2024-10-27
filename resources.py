# main.py
import get_all_resources
import teraform_build_resources

from flask import Flask, request, jsonify

app = Flask(__name__)


# Get endpoint to retrieve all users
@app.route('/resources', methods=['Get'])
def get_resources():

    display_all_resources = []

    # Call get all resources by boto3
    get_all_resources.list_rds_instances()
    get_all_resources.list_s3_buckets()
    get_all_resources.list_lambda_functions()

    for resource in get_all_resources.resources:
       display_all_resources.append({ 'Service' : resource['Service'], 'ARN' : resource['ARN'] })       

    # display resources { { Service: %Service-name%, ARN: %Service-ARN% } }
    return jsonify(display_all_resources)

# Post endpoint for create new resources
@app.route('/resources', methods=['Post'])
def create_resources():
    data = request.get_json()
    
     # Extract parameters from the request body
    bucket_name = data.get("bucket_name")
    lambda_name = data.get("lambda_name")
    lambda_role_arn = data.get("lambda_role_arn")
    lambda_zip_file = data.get("lambda_zip_file")
    db_name = data.get("db_name")
    db_username = data.get("db_username")
    db_password = data.get("db_password")

    is_valid = True
    errors_list = []
    if not bucket_name or bucket_name == "":
        is_valid = False
        errors_list.append({"error": "Bucket name is required"})
    
    if not lambda_name or lambda_name == "":
        is_valid = False
        errors_list.append({"error": "Lambda name is required"})
    
    if not lambda_role_arn or lambda_role_arn == "":
        is_valid = False
        errors_list.append({"error": "Lambda role arn is required"})
    
    if not lambda_zip_file or lambda_zip_file == "":
        is_valid = False
        errors_list.append({"error": "Lambda zip file is required"})
    
    if not db_name or db_name == "":
        is_valid = False
        errors_list.append({"error": "Database name is required"})
    
    if not db_username or db_username == "":
        is_valid = False
        errors_list.append({"error": "Database username is required"})
    
    if not db_password or db_password == "":
        is_valid = False
        errors_list.append({"error": "Database passowrd is required"})
        
    # Validation checking
    if is_valid == False:
        # Display errors on invalid inputs 
        return jsonify(errors_list), 400
    
    # Run Terraform commands
    teraform_build_resources.terraform_init()
    teraform_build_resources.terraform_apply(
        bucket_name, 
        lambda_name, 
        lambda_role_arn, 
        lambda_zip_file, 
        db_name, 
        db_username, 
        db_password
    )

    # Get output and send it back
    output = teraform_build_resources.terraform_output()
    return jsonify({"status": "Resources created", "output": output})

# Post endpoint for create new resources
@app.route('/resource', methods=['Delete'])
def delete_resource():
    data = request.get_json()
    resource_name = data.get("resource_name")    

    if not resource_name or resource_name == "":
        return jsonify({"error": "Resource name is required"}), 400

    # Run Terraform commands to delete the specified resource
    teraform_build_resources.terraform_init()
    teraform_build_resources.terraform_destroy(resource_name)

    return jsonify({"status": "Resource deleted", "resource_name": resource_name})


# Main - function
if __name__ ==  '__main__':
    app.run(debug=True)