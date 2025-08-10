Feature: Validate and format JSON files before uploading to Azure Blob Storage

  As a developer,
  I want uploaded JSON files to be validated and formatted before being stored in Azure Blob Storage,
  So that downstream services can reliably read them.

  Scenario: Uploading a valid and already formatted JSON file
    Given I have a valid and properly formatted JSON file at "tests/data/formatted.json"
    When I upload the file "tests/data/formatted.json" to "valid-json-container"
    Then the file should be uploaded successfully
    And the contents should match the original file exactly

  Scenario: Uploading a valid but unformatted JSON file
    Given I have a valid but poorly formatted JSON file at "tests/data/unformatted.json"
    When I upload the file "tests/data/unformatted.json" to "valid-json-container"
    Then the file should be uploaded successfully
    And the contents in Azure should be properly formatted JSON

  Scenario: Uploading an invalid JSON file
    Given I have an invalid JSON file at "tests/data/invalid.json"
    When I upload the file "tests/data/invalid.json" to "valid-json-container"
    Then the upload should fail
    And I should receive an error message indicating the JSON is invalid

  Scenario: Uploading a non-JSON file
    Given I have a non-JSON file at "tests/data/image.png"
    When I upload the file "tests/data/image.png" to "valid-json-container"
    Then the upload should fail
    And I should receive an error message indicating unsupported file type
