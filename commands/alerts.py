import click
from api import api_create_alert, api_list_alerts, api_show_alert
from utils import display_paginated_results, handle_api_error, format_item_details

@click.group()
def alerts():
    """Commands for managing PagerTree alerts."""
    pass

@alerts.command(name="create")
@click.option("--title", required=True, help="Title of the alert")
@click.option("--description", help="Description of the alert")
def create_alert_cmd(title, description):
    """Create a new alert in PagerTree."""
    try:
        result = api_create_alert(title, description or "No description provided")
        click.echo(f"Alert created successfully: {result.get('id')}")
    except Exception as e:
        click.echo(f"Error creating alert: {str(e)}", err=True)

@alerts.command(name="list")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of alerts per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
def list_alerts_cmd(limit, offset):
    """List alerts in PagerTree with pagination."""
    try:
        result = api_list_alerts(limit=limit, offset=offset)
        alerts_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Title", "Status"]
        table_data = [[alert.get("tiny_id"), alert.get("title"), alert.get("status")] for alert in alerts_list]
        display_paginated_results(alerts_list, total, limit, offset, "alert", headers, table_data)
    except Exception as e:
        handle_api_error(e, action="listing alerts")

@alerts.command(name="show")
@click.argument("alert_id", required=True)
def show_alert_cmd(alert_id):
    """Show details of a specific alert in PagerTree."""
    try:
        alert = api_show_alert(alert_id)
        fields = {
            "id": "Alert ID",
            "title": "Title",
            "description": "Description",
            "status": "Status",
            "created_at": "Created At"
        }
        format_item_details(alert, fields)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error fetching alert: {e.response.status_code} - {e.response.reason}", err=True)
    except Exception as e:
        handle_api_error(e, "showing alert")