import click
import requests
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

def format_item_details(item, fields):
    """Format and display item details as a table using tabulate."""
    # Prepare table data: each row is [Display Name, Value]
    table_data = [
        [display_name, item.get(field_name, "N/A")]
        for field_name, display_name in fields.items()
    ]
    # Define table headers
    headers = ["Field", "Value"]
    # Display the table using tabulate with github format
    click.echo(tabulate(table_data, headers=headers, tablefmt="simple", maxcolwidths=[None, 50]))