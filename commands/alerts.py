import click
import json
from utils import display_paginated_results, handle_api_error, format_item_details

@click.group()
def alerts():
    """Commands for managing PagerTree alerts."""
    pass

@alerts.command(name="create")
@click.option("--title", required=True, help="Title of the alert")
@click.option("--description", help="Description of the alert")
@click.option("--team-id", "team_ids", multiple=True, help="Team IDs to route the alert to")
@click.option("--urgency", type=click.Choice(["silent", "low", "medium", "high", "critical"]), default="medium", help="Priority of the alert")
@click.option("--tags", multiple=True, help="Tags for the alert")
@click.option("--alias", help="Alias for the alert")
@click.pass_context
def create_alert_cmd(ctx, title, description, team_ids, urgency, tags, alias):
    """Create a new alert in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.create_alert(
            title=title,
            description=description,
            team_ids=list(team_ids),
            urgency=urgency,
            tags=list(tags),
            alias=alias
        )
        click.echo(f"Alert created successfully: {result.get('id')}")
    except Exception as e:
        handle_api_error(e, action="creating alert")

@alerts.command(name="list")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of alerts per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.option("--status", type=click.Choice(["open", "acknowledged", "resolved", "dropped"]), help="Filter alerts by status")
@click.option("--search", help="Search for alerts by title, tags, source, or destinations")
@click.pass_context
def list_alerts_cmd(ctx, limit, offset, status, search):
    """List alerts in PagerTree with pagination."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        logger = ctx.obj.logger  # Get logger from context
        logger.debug(f"Listing alerts with limit={limit}, offset={offset}, status={status}, search={search}")
        result = client.list_alerts(limit=limit, offset=offset, status=status, search=search)
        logger.debug(f"Full response: {json.dumps(result, indent=2)}")
        alerts_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Title", "Status"]
        table_data = [[alert.get("id"), alert.get("title"), alert.get("status")] for alert in alerts_list]
        display_paginated_results(alerts_list, total, limit, offset, "alert", headers, table_data)
    except Exception as e:
        logger.error(f"Error listing alerts: {str(e)}")
        handle_api_error(e, action="listing alerts")

@alerts.command(name="show")
@click.argument("alert_id", required=True)
@click.pass_context
def show_alert_cmd(ctx, alert_id):
    """Show details of a specific alert in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        alert = client.show_alert(alert_id)
        fields = {
            "id": "ID",
            "status": "Status",
            "urgency": "Urgency",
            "tags": "Tags",            
            "thirdparty_id": "Third Party ID",
            "destination_team_ids": "Destination Team IDs",
            "destination_router_ids": "Destination Router IDs",
            "destination_account_user_ids": "Destination Account User IDs",
            "title": "Title",
            "description": "Description",
            "created_at": "Created At"
        }
        format_item_details(alert, fields)
    except Exception as e:
        handle_api_error(e, "showing alert")

@alerts.command(name="delete")
@click.argument("alert_id", required=True)
@click.option("--force", is_flag=True, help="Delete the alert without confirmation")
@click.pass_context
def delete_alert_cmd(ctx, alert_id, force):
    """Delete an alert in PagerTree."""
    if not force and not click.confirm(f"Are you sure you want to delete alert {alert_id}?"):
        click.echo("Deletion cancelled.")
        return
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.delete_alert(alert_id)
        click.echo(f"Alert deleted successfully: {alert_id}")
    except Exception as e:
        handle_api_error(e, action="deleting alert")

@alerts.command(name="acknowledge")
@click.argument("alert_id", required=False)  # Make alert_id optional
@click.option("--alias", help="Alias for the alert")
@click.pass_context
def acknowledge_alert_cmd(ctx, alert_id, alias):
    """Acknowledge an alert in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context

        # Ensure at least one of alert_id or alias is provided
        if not alert_id and not alias:
            click.echo("Error: Either alert_id or alias must be provided.")
            return

        # If alias is provided, resolve it to alert_id
        if alias:
            alias_result = client.list_alerts(alias=alias, limit=1, offset=0)
            if alias_result["total"] == 0:
                click.echo(f"No alert found with alias: {alias}")
                return
            alert_id = alias_result["data"][0]["id"]

        # If alert_id is still not set, raise an error
        if not alert_id:
            click.echo("Error: Could not resolve alert_id.")
            return

        result = client.acknowledge_alert(alert_id)
        click.echo(f"Alert acknowledged successfully: {result.get('id')}")
    except Exception as e:
        handle_api_error(e, action="acknowledging alert")

@alerts.command(name="reject")
@click.argument("alert_id", required=False)  # Make alert_id optional
@click.option("--alias", help="Alias for the alert")
@click.pass_context
def reject_alert_cmd(ctx, alert_id, alias):
    """Reject an alert in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context

        # Ensure at least one of alert_id or alias is provided
        if not alert_id and not alias:
            click.echo("Error: Either alert_id or alias must be provided.")
            return

        # If alias is provided, resolve it to alert_id
        if alias:
            alias_result = client.list_alerts(alias=alias, limit=1, offset=0, status="open")
            if alias_result["total"] == 0:
                click.echo(f"No alert found with alias: {alias}")
                return
            alert_id = alias_result["data"][0]["id"]

        # If alert_id is still not set, raise an error
        if not alert_id:
            click.echo("Error: Could not resolve alert_id.")
            return

        result = client.reject_alert(alert_id)
        click.echo(f"Alert rejected successfully: {result.get('id')}")
    except Exception as e:
        handle_api_error(e, action="rejecting alert")

@alerts.command(name="resolve")
@click.argument("alert_id", required=False)  # Make alert_id optional
@click.option("--alias", help="Alias for the alert")
@click.pass_context
def resolve_alert_cmd(ctx, alert_id, alias):
    """Resolve an alert in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context

        # Ensure at least one of alert_id or alias is provided
        if not alert_id and not alias:
            click.echo("Error: Either alert_id or alias must be provided.")
            return

        # If alias is provided, resolve it to alert_id
        if alias:
            alias_result = client.list_alerts(alias=alias, limit=1, offset=0)
            if alias_result["total"] == 0:
                click.echo(f"No alert found with alias: {alias}")
                return
            alert_id = alias_result["data"][0]["id"]

        # If alert_id is still not set, raise an error
        if not alert_id:
            click.echo("Error: Could not resolve alert_id.")
            return

        result = client.resolve_alert(alert_id)
        click.echo(f"Alert resolved successfully: {result.get('id')}")
    except Exception as e:
        handle_api_error(e, action="resolving alert")

@alerts.command(name="list-comments")
@click.argument("alert_id", required=False)  # Make alert_id optional
@click.option("--alias", help="Alias for the alert")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of alerts per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.pass_context
def list_alert_comment_cmd(ctx, alert_id, alias, limit, offset):
    """List an alert's comments in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context

        # Ensure at least one of alert_id or alias is provided
        if not alert_id and not alias:
            click.echo("Error: Either alert_id or alias must be provided.")
            return

        # If alias is provided, resolve it to alert_id
        if alias:
            alias_result = client.list_alerts(alias=alias, limit=1, offset=0)
            if alias_result["total"] == 0:
                click.echo(f"No alert found with alias: {alias}")
                return
            alert_id = alias_result["data"][0]["id"]

        # If alert_id is still not set, raise an error
        if not alert_id:
            click.echo("Error: Could not resolve alert_id.")
            return

        result = client.list_alert_comments(alert_id, limit=limit, offset=offset)
        comments_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["Created At", "Commentor", "Comment"]
        table_data = [[comment.get("created_at"), comment.get("created_by_name"), comment.get("body")] for comment in comments_list]
        display_paginated_results(comments_list, total, limit, offset, "comment", headers, table_data)
    except Exception as e:
        handle_api_error(e, action="listing alert comments")

@alerts.command(name="comment")
@click.argument("alert_id", required=False)  # Make alert_id optional
@click.option("--alias", help="Alias for the alert")
@click.option("--comment", required=True, help="Comment to add to the alert")
@click.pass_context
def create_alert_comment_cmd(ctx, alert_id, alias, comment):
    """Add a comment to an alert in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context

        # Ensure at least one of alert_id or alias is provided
        if not alert_id and not alias:
            click.echo("Error: Either alert_id or alias must be provided.")
            return

        # If alias is provided, resolve it to alert_id
        if alias:
            alias_result = client.list_alerts(alias=alias, limit=1, offset=0)
            if alias_result["total"] == 0:
                click.echo(f"No alert found with alias: {alias}")
                return
            alert_id = alias_result["data"][0]["id"]

        # If alert_id is still not set, raise an error
        if not alert_id:
            click.echo("Error: Could not resolve alert_id.")
            return

        result = client.create_alert_comment(alert_id, comment)
        click.echo(f"Comment added successfully to alert {alert_id}")
    except Exception as e:
        handle_api_error(e, action="adding comment to alert")

