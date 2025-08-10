
# features/steps/upload_steps.py
import os
import json
from behave import given, when, then
from features.uploader import JsonUploader

@given('I have a valid and properly formatted JSON file at "{file_path}"')
@given('I have a valid but poorly formatted JSON file at "{file_path}"')
@given('I have an invalid JSON file at "{file_path}"')
@given('I have a non-JSON file at "{file_path}"')
def step_given_file_exists(context, file_path):
    assert os.path.exists(file_path), f"File does not exist: {file_path}"
    context.file_path = file_path
    context.uploader = JsonUploader()

@when('I upload the file "{file_path}" to "{container_name}"')
def step_when_upload_file(context, file_path, container_name):
    try:
        path = context.uploader.upload(file_path, container_name)
        context.upload_result = path
        context.upload_success = True
    except Exception as e:
        context.upload_success = False
        context.upload_error = str(e)

@then('the file should be uploaded successfully')
def step_then_uploaded_successfully(context):
    assert context.upload_success is True

@then('the contents should match the original file exactly')
def step_then_contents_match(context):
    with open(context.file_path, "r") as original:
        original_data = json.load(original)

    with open(context.upload_result, "r") as uploaded:
        uploaded_data = json.load(uploaded)

    assert original_data == uploaded_data, "Uploaded JSON content does not match the original data"

@then('the contents in Azure should be properly formatted JSON')
def step_then_contents_are_formatted(context):
    with open(context.upload_result, "r") as f:
        formatted = f.read()
    try:
        parsed = json.loads(formatted)
    except Exception as e:
        assert False, f"Uploaded file is not valid JSON: {e}"

    re_formatted = json.dumps(parsed, indent=2, sort_keys=True)
    assert formatted == re_formatted

@then('the upload should fail')
def step_then_upload_should_fail(context):
    assert context.upload_success is False

@then('I should receive an error message indicating the JSON is invalid')
def step_then_invalid_json_error(context):
    assert "Invalid JSON" in context.upload_error

@then('I should receive an error message indicating unsupported file type')
def step_then_invalid_type_error(context):
    assert "Unsupported file type" in context.upload_error
