import click
from utils import display_paginated_results, handle_api_error, format_item_details
from datetime import datetime

@click.group()
def broadcasts():
    """Commands for managing PagerTree broadcasts."""
    pass

@broadcasts.command(name="create")
@click.option("--title", required=True, help="Title of the broadcast")
@click.option("--description", help="Description of the broadcast")
@click.option("--user-id", "user_ids", multiple=True, help="Account user IDs to receive the broadcast")
@click.option("--team-id", "team_ids", multiple=True, help="Team IDs to receive the broadcast")
@click.pass_context
def create_broadcast_cmd(
    ctx, title, description, user_ids, team_ids
):
    """Create a new broadcast in PagerTree."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        result = client.create_broadcast(
            title=title,
            description=description,
            destination_account_user_ids=list(user_ids) if user_ids else None,
            destination_team_ids=list(team_ids) if team_ids else None
        )
        click.echo(f"Broadcast created successfully: {result.get('id', 'N/A')}")
    except Exception as e:
        handle_api_error(e, action="creating broadcast")

@broadcasts.command(name="list")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of broadcasts per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.pass_context
def list_broadcasts_cmd(ctx, limit, offset):
    """List broadcasts in PagerTree with pagination."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        result = client.list_broadcasts(limit=limit, offset=offset)
        broadcasts_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Title", "Status", "Created At"]
        table_data = [
            [
                broadcast.get("id", "N/A"),
                broadcast.get("title", "N/A"),
                broadcast.get("status", "N/A"),
                broadcast.get("created_at", "N/A")
            ]
            for broadcast in broadcasts_list
        ]
        display_paginated_results(broadcasts_list, total, limit, offset, "broadcast", headers, table_data)
    except Exception as e:
        handle_api_error(e, action="listing broadcasts")

@broadcasts.command(name="show")
@click.argument("broadcast_id", required=True)
@click.pass_context
def show_broadcast_cmd(ctx, broadcast_id):
    """Show details of a specific broadcast in PagerTree."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        broadcast = client.show_broadcast(broadcast_id)
        fields = {
            "id": "Broadcast ID",
            "title": "Title",
            "description": "Description",
            "status": "Status"
        }
        formatted_broadcast = {
            "id": broadcast.get("id", "N/A"),
            "title": broadcast.get("title", "N/A"),
            "description": broadcast.get("description", "N/A"),
            "status": broadcast.get("status", "N/A")
        }
        format_item_details(formatted_broadcast, fields)
    except Exception as e:
        handle_api_error(e, action="showing broadcast")

@broadcasts.command(name="delete")
@click.argument("broadcast_id", required=True)
@click.option("--force", is_flag=True, help="Delete the broadcast without confirmation")
@click.pass_context
def delete_broadcast_cmd(ctx, broadcast_id, force):
    """Delete a broadcast in PagerTree."""
    if not force and not click.confirm(f"Are you sure you want to delete broadcast {broadcast_id}?"):
        click.echo("Deletion cancelled.")
        return
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        result = client.delete_broadcast(broadcast_id)
        click.echo(f"Broadcast deleted successfully: {broadcast_id}")
    except Exception as e:
        handle_api_error(e, action="deleting broadcast")