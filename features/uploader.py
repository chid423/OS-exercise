# features/uploader.py

import json
import os

class JsonUploader:
    def __init__(self, storage_path="mock_blob_storage"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def is_json_file(self, file_path):
        return file_path.endswith(".json")

    def validate_json(self, file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None

    def format_json(self, data):
        return json.dumps(data, indent=2, sort_keys=True)

    def upload(self, file_path, container_name):
        if not self.is_json_file(file_path):
            raise ValueError("Unsupported file type")

        data = self.validate_json(file_path)
        if data is None:
            raise ValueError("Invalid JSON")

        formatted_content = self.format_json(data)

        container_path = os.path.join(self.storage_path, container_name)
        os.makedirs(container_path, exist_ok=True)

        filename = os.path.basename(file_path)
        target_path = os.path.join(container_path, filename)

        with open(target_path, "w") as f:
            f.write(formatted_content)

        return target_path
