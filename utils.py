import click
import requests
from tabulate import tabulate

def display_paginated_results(items, total, limit, offset, item_type="item", table_headers=None, table_data=None):
    """Display a paginated list of items with consistent formatting."""
    click.echo(f"Showing {len(items)} of {total} {item_type}s (offset: {offset}, limit: {limit})")
    if table_headers and table_data:
        click.echo(tabulate(table_data, headers=table_headers, tablefmt="github"))
    if offset + limit < total:
        click.echo(f"More {item_type}s available. Use --offset {offset + limit} to see next page.")

def handle_api_error(e, action="performing action"):
    """Handle API errors with consistent messaging."""
    if isinstance(e, requests.exceptions.HTTPError):
        click.echo(f"Error {action}: {e.response.status_code} - {e.response.reason}", err=True)
    else:
        click.echo(f"Error {action}: {str(e)}", err=True)

def format_item_details(item, fields):
    """Format and display item details from a dict with specified fields."""
    for field_name, display_name in fields.items():
        value = item.get(field_name, "N/A")
        click.echo(f"{display_name}: {value}")