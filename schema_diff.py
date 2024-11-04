import requests
from graphql import build_ast_schema, parse, GraphQLSchema
import os
from mistralai import Mistral



# Your API token for accessing Mistral's hosted API
token = "b3gNQMwOtDs1mHDVMJMjTAEgy1uS82oj"
client = Mistral(api_key=token)


def parse_schema(schema_str: str) -> GraphQLSchema:
    return build_ast_schema(parse(schema_str))

def find_breaking_changes(old_schema: GraphQLSchema, new_schema: GraphQLSchema):


    breaking_changes = []
    # Check for removed types

    for type_name in old_schema.type_map:
        if type_name not in new_schema.type_map:
            breaking_changes.append({
                "type": "type_removed",
                "description": f"Type '{type_name}' was removed.",
                "path": type_name
            })


    # Check for removed fields
    for type_name, old_type in old_schema.type_map.items():
        if type_name in new_schema.type_map:
            new_type = new_schema.type_map[type_name]
            if hasattr(old_type, 'fields') and hasattr(new_type, 'fields'):
                old_fields = old_type.fields
                new_fields = new_type.fields
                for field_name in old_fields:
                    if field_name not in new_fields:
                        breaking_changes.append({
                            "type": "field_removed",
                            "description": f"Field '{field_name}' was removed from type '{type_name}'.",
                            "path": f"{type_name}.{field_name}"
                        })
    return breaking_changes


    non_breaking_changes = []

    # Check for added types
    for type_name in new_schema.type_map:
        if type_name not in old_schema.type_map:
            non_breaking_changes.append({
                "type": "type_added",
                "description": f"Type '{type_name}' was added.",
                "path": type_name
            })

    # Check for added fields
    for type_name, new_type in new_schema.type_map.items():
        if type_name in old_schema.type_map:
            old_type = old_schema.type_map[type_name]
            if hasattr(old_type, 'fields') and hasattr(new_type, 'fields'):
                new_fields = new_type.fields
                old_fields = old_type.fields
                for field_name in new_fields:
                    if field_name not in old_fields:
                        non_breaking_changes.append({
                            "type": "field_added",
                            "description": f"Field '{field_name}' was added to type '{type_name}'.",
                            "path": f"{type_name}.{field_name}"
                        })

    # Check for added arguments in existing fields
    for type_name, new_type in new_schema.type_map.items():
        if type_name in old_schema.type_map:
            old_type = old_schema.type_map[type_name]
            if hasattr(old_type, 'fields') and hasattr(new_type, 'fields'):
                for field_name, new_field in new_type.fields.items():
                    if field_name in old_type.fields:
                        old_field = old_type.fields[field_name]
                        if hasattr(old_field, 'args') and hasattr(new_field, 'args'):
                            new_args = new_field.args
                            old_args = old_field.args
                            for arg_name in new_args:
                                if arg_name not in old_args:
                                    non_breaking_changes.append({
                                        "type": "argument_added",
                                        "description": f"Argument '{arg_name}' was added to field '{field_name}' in type '{type_name}'.",
                                        "path": f"{type_name}.{field_name}({arg_name})"
                                    })

    return non_breaking_changes


def find_non_breaking_changes(old_schema: GraphQLSchema, new_schema: GraphQLSchema):
    non_breaking_changes = []

    # Check for added types
    for type_name in new_schema.type_map:
        if type_name not in old_schema.type_map:
            non_breaking_changes.append({
                "type": "type_added",
                "description": f"Type '{type_name}' was added.",
                "path": type_name
            })

    # Check for added fields
    for type_name, new_type in new_schema.type_map.items():
        if type_name in old_schema.type_map:
            old_type = old_schema.type_map[type_name]
            if hasattr(old_type, 'fields') and hasattr(new_type, 'fields'):
                new_fields = new_type.fields
                old_fields = old_type.fields
                for field_name in new_fields:
                    if field_name not in old_fields:
                        non_breaking_changes.append({
                            "type": "field_added",
                            "description": f"Field '{field_name}' was added to type '{type_name}'.",
                            "path": f"{type_name}.{field_name}"
                        })

    # Check for added arguments in existing fields
    for type_name, new_type in new_schema.type_map.items():
        if type_name in old_schema.type_map:
            old_type = old_schema.type_map[type_name]
            if hasattr(old_type, 'fields') and hasattr(new_type, 'fields'):
                for field_name, new_field in new_type.fields.items():
                    if field_name in old_type.fields:
                        old_field = old_type.fields[field_name]
                        if hasattr(old_field, 'args') and hasattr(new_field, 'args'):
                            new_args = new_field.args
                            old_args = old_field.args
                            for arg_name in new_args:
                                if arg_name not in old_args:
                                    non_breaking_changes.append({
                                        "type": "argument_added",
                                        "description": f"Argument '{arg_name}' was added to field '{field_name}' in type '{type_name}'.",
                                        "path": f"{type_name}.{field_name}({arg_name})"
                                    })

    return non_breaking_changes



def format_diff_as_json(breaking_changes):
    return {"breaking_changes": breaking_changes}

def convert_json_to_text(json_input):
    """
    Convert a JSON object or JSON file to a formatted text string.
    
    Args:
    - json_input (str or dict): A JSON string, JSON file path, or JSON object (dict).
    
    Returns:
    - str: A formatted string representation of the JSON content.
    """
    
    # Check if the input is a string and might be a file path
    if isinstance(json_input, str):
        try:
            with open(json_input, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If not a file, treat it as a JSON string
            data = json.loads(json_input)
    elif isinstance(json_input, dict):
        data = json_input
    else:
        raise ValueError("Input must be a JSON string, JSON file path, or dictionary.")
    
    # Function to recursively convert JSON to text
    def json_to_text(data, indent=0):
        result = ""
        spacing = "  " * indent  # Indentation for nested structures
        
        if isinstance(data, dict):
            for key, value in data.items():
                result += f"{spacing}{key}: "
                result += json_to_text(value, indent + 1)
        elif isinstance(data, list):
            for item in data:
                result += f"{spacing}- {json_to_text(item, indent + 1)}"
        else:
            result += str(data) + "\n"
        
        return result
def generate_release_notes_with_mistral_breaking(changes_json):
    # Prepare the input data as a formatted prompt
    breaking_changes = changes_json.get("breaking_changes", [])
   

    
    breaking_summary = "\n".join(
        f"- **{change['type']}**: {change['description']}" for change in breaking_changes
    ) or "No breaking changes."
    
    
    prompt = f"""
    You are a release notes generator. Here is a list of changes between two versions of a GraphQL schema:
    
    ## Breaking Changes
    {breaking_summary}


     Based on this information, generate a structured, human-readable release note document to describe breaking changes. Take out all 
    special characters and write in full sentences. Keep the note concise and to the point.
    """

    # API request payload
    model = "ministral-3b-latest"



    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    
    print('chat_response.choices[0].message.content:', chat_response.choices[0].message.content)
    return chat_response.choices[0].message.content
    
def generate_release_notes_with_mistral_non_breaking(changes_json):
    # Prepare the input data as a formatted prompt
    print('changes_json:', changes_json)
    non_breaking_changes = changes_json.get("breaking_changes", [])
    print('non_breaking_changes:', non_breaking_changes)
    
    if non_breaking_changes and any("description" in change for change in non_breaking_changes):
        non_breaking_summary = "\n".join(
            f"- **{change['type']}**: {change['description']}"
            for change in non_breaking_changes if 'description' in change
        )
    else:
        non_breaking_summary = "No non-breaking changes."

    print('non_breaking_summary:', non_breaking_summary)
    
    prompt = f"""
    You are a release notes generator. Here is a list of changes between two versions of a GraphQL schema:
    
    ## Non-Breaking Changes
    {non_breaking_summary}

    Based on this information, generate a structured, human-readable release note document to describe non-breaking changes. Take out all 
    special characters and write in full sentences. Keep the note concise and to the point.
    
    """

    # API request payload
    model = "ministral-3b-latest"



    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    
    print('chat_response.choices[0].message.content:', chat_response.choices[0].message.content)
    return chat_response.choices[0].message.content
