 Schema Diff API

This is a FastAPI-based service that analyzes two versions of a schema and provides a comparison of the differences. It identifies breaking and non-breaking changes, formats these differences in JSON, and generates release notes for each category.

## Features

- **Breaking Changes Detection**: Identifies breaking changes between two schema versions.
- **Non-Breaking Changes Detection**: Identifies non-breaking changes between schema versions.
- **Formatted Output**: Provides JSON-formatted output for breaking and non-breaking changes.
- **Release Notes Generation**: Generates release notes for both breaking and non-breaking changes using a tool named Mistral.

## Endpoints

### `POST /diff/`

Analyzes two schema versions and returns differences as well as generated release notes.

- **Request Parameters**:
  - `schema1` (string): The first schema (old version) to compare.
  - `schema2` (string): The second schema (new version) to compare.

- **Response**:
  - **200 OK**: Successful schema comparison.
    - **breaking_changes**: Details of breaking changes.
      - `json_output`: JSON representation of the breaking changes.
      - `release_notes`: Generated release notes for breaking changes.
    - **non_breaking_changes**: Details of non-breaking changes.
      - `json_output`: JSON representation of the non-breaking changes.
      - `release_notes`: Generated release notes for non-breaking changes.

  - **400 Bad Request**: Error encountered while parsing or processing schemas.

Example response:
```json
{
  "breaking_changes": {
    "json_output": { ... },
    "release_notes": "..."
  },
  "non_breaking_changes": {
    "json_output": { ... },
    "release_notes": "..."
  }
}
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/schema-diff-api.git
   cd schema-diff-api
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

To use the `/diff/` endpoint, send a `POST` request with JSON payload containing `schema1` and `schema2` strings.

### Example

```bash
curl -X POST "http://127.0.0.1:8000/diff/" -H "Content-Type: application/json" -d '{
  "schema1": "...",
  "schema2": "..."
}'
```

## Error Handling

If an error occurs (e.g., invalid schema), the endpoint will respond with a `400` status code and a detailed error message.

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **parsers**: Custom module to parse schemas.
- **schema_diff**: Custom module with functions to find breaking and non-breaking changes, format JSON, and generate release notes with Mistral.

## Project Structure

- `main.py`: Defines the FastAPI application and `/diff/` endpoint.
- `parsers.py`: Contains functions for schema parsing.
- `schema_diff.py`: Contains functions to find schema differences, format JSON, and generate release notes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- **Mistral**: Used for generating release notes.
