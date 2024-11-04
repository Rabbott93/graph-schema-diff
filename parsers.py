from graphql import build_ast_schema, parse

def parse_schema(schema_str: str):
    return build_ast_schema(parse(schema_str))
