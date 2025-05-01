import click
import requests
from typing import Dict, Any
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError, JsonPathLexerError
from tabulate import tabulate

def handle_api_error(e, action="performing action"):
    """Handle API errors with consistent messaging."""
    if isinstance(e, requests.exceptions.HTTPError):
        try:
            response_json = e.response.json()
            errors = response_json.get("errors", "No error details provided")
            click.echo(f"Error {action}: {e.response.status_code} - {errors}", err=True)
        except ValueError:
            # Handle case where response is not JSON
            click.echo(f"Error {action}: {e.response.status_code} - Unable to parse error details", err=True)
    else:
        click.echo(f"Error {action}: {str(e)}", err=True)

def display_paginated_results(items, total, limit, offset, item_type="item", table_headers=None, table_data=None):
    """Display a paginated list of items with consistent formatting."""
    click.echo(f"Showing {len(items)} of {total} {item_type}s (offset: {offset}, limit: {limit})")
    if table_headers and table_data:
        click.echo(tabulate(table_data, headers=table_headers, tablefmt="simple", maxcolwidths=[None, 50]))
    if offset + limit < total:
        click.echo(f"More {item_type}s available. Use --offset {offset + limit} to see next page.")

def format_item_details(item: Dict[str, Any], fields: Dict[str, str]) -> None:
    """Format and display item details as a table using tabulate, supporting JSON path notation."""
    # Prepare table data: each row is [Display Name, Value]
    table_data = []
    for field_path, display_name in fields.items():
        try:
            # Try to parse the field_path as a JSON path
            jsonpath_expr = parse(field_path)
            matches = jsonpath_expr.find(item)
            value = matches[0].value if matches else "N/A"
        except (JsonPathParserError, JsonPathLexerError, IndexError, KeyError):
            # Fallback to direct dictionary access for simple field names
            value = item.get(field_path, "N/A")

        # Format specific types for better readability
        if isinstance(value, bool):
            value = "Yes" if value else "No"
        elif isinstance(value, list):
            value = ", ".join(str(v) for v in value) if value else "None"
        elif isinstance(value, dict):
            value = str(value)  # Convert dict to string for simplicity
        elif value is None:
            value = "N/A"
        
        table_data.append([display_name, value])
    
    # Define table headers
    headers = ["Field", "Value"]
    # Display the table using tabulate with simple format
    click.echo(tabulate(table_data, headers=headers, tablefmt="simple", maxcolwidths=[None, 50]))