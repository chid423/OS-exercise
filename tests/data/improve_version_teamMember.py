
def upload_and_save_file(service_client, name, filepath):
    try:
        with open(filepath, "r") as f:
            data = f.read()
        blob_client = service_client.get_blob_client(container=name, blob=filepath)
        blob_client.upload_blob(data)
    except Exception:
        return False








import json
from azure.storage.blob import ContentSettings

def upload_and_save_file(service_client, container_name, blob_name, filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        formatted = json.dumps(data, indent=2)

        blob_client = service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(
            formatted,
            overwrite=True,
            content_settings=ContentSettings(content_type='application/json')
        )
    except FileNotFoundError:
        raise ValueError(f"File not found: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in file: {filepath}")
