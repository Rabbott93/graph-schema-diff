from fastapi import FastAPI, HTTPException
from parsers import parse_schema
from schema_diff import find_breaking_changes, find_non_breaking_changes, format_diff_as_json, generate_release_notes_with_mistral_breaking, generate_release_notes_with_mistral_non_breaking

app = FastAPI()

@app.post("/diff/")
async def get_diff(schema1: str, schema2: str):
    try:
        # Parse the schemas
        old_schema = parse_schema(schema1)
        new_schema = parse_schema(schema2)

        # Compute the breaking changes
        breaking_changes = find_breaking_changes(old_schema, new_schema)

        # Compute the non-breaking changes
        non_breaking_changes = find_non_breaking_changes(old_schema, new_schema)

        # Format the diff results
        json_output_breaking = format_diff_as_json(breaking_changes)
        json_output_non_breaking = format_diff_as_json(non_breaking_changes)
      
    
        # Generate release notes
        release_notes_breaking = generate_release_notes_with_mistral_breaking(json_output_breaking)
        release_notes_non_breaking = generate_release_notes_with_mistral_non_breaking(json_output_non_breaking)

        return {
            "breaking_changes": {
                "json_output": json_output_breaking,
                "release_notes": release_notes_breaking
            },
            "non_breaking_changes": {
                "json_output": json_output_non_breaking,
                "release_notes": release_notes_non_breaking
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
