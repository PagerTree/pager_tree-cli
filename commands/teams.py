import click
from tabulate import tabulate
from utils import display_paginated_results, handle_api_error, format_item_details

@click.group()
def teams():
    """Commands for managing PagerTree teams."""
    pass

@teams.command(name="create")
@click.option("--name", required=True, help="Name of the team")
@click.option("--notes", help="Notes for the team")
@click.option("--member-id", "member_ids", multiple=True, help="Account user IDs to add as team members")
@click.option("--admin-id", "admin_ids", multiple=True, help="Account user IDs to add as team admins")
@click.pass_context
def create_team_cmd(ctx, name, notes, member_ids, admin_ids):
    """Create a new team in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.create_team(
            name=name,
            notes=notes,
            member_account_user_ids=list(member_ids) if member_ids else None,
            admin_account_user_ids=list(admin_ids) if admin_ids else None
        )
        click.echo(f"Team created successfully: {result.get('id', 'N/A')}")
    except Exception as e:
        handle_api_error(e, action="creating team")

@teams.command(name="list")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of teams per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.option("--search", help="Search for teams by name")
@click.pass_context
def list_teams_cmd(ctx, limit, offset, search):
    """List teams in PagerTree with pagination."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.list_teams(limit=limit, offset=offset, search=search)
        teams_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Name"]
        table_data = [
            [
                team.get("id", "N/A"),
                team.get("name", "N/A")
            ]
            for team in teams_list
        ]
        display_paginated_results(teams_list, total, limit, offset, "team", headers, table_data)
    except Exception as e:
        handle_api_error(e, action="listing teams")

@teams.command(name="show")
@click.argument("team_id", required=True)
@click.pass_context
def show_team_cmd(ctx, team_id):
    """Show details of a specific team in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        team = client.show_team(team_id)
        
        # Display team details
        fields = {
            "id": "Team ID",
            "name": "Name",
            "notes": "Notes",
            "created_at": "Created At",
            "updated_at": "Updated At"
        }
        formatted_team = {
            "id": team.get("id", "N/A"),
            "name": team.get("name", "N/A"),
            "notes": team.get("notes", "N/A"),
            "created_at": team.get("created_at", "N/A"),
            "updated_at": team.get("updated_at", "N/A")
        }
        click.echo("Team Details:")
        format_item_details(formatted_team, fields)
        
        # Fetch and display team members
        members = team.get("member_account_user_ids", [])
        if not members:
            click.echo("\nTeam Members: None")
        else:
            member_details = []
            for member_id in members:
                try:
                    user = client.show_user(member_id)
                    user_data = user.get("user", {})
                    member_details.append({
                        "id": user.get("id", "N/A"),
                        "name": user_data.get("name", "N/A"),
                        "emails": user_data.get("emails", []),
                        "phones": user_data.get("phones", [])
                    })
                except Exception as e:
                    click.echo(f"Warning: Could not fetch details for member {member_id}: {str(e)}", err=True)
            
            if not member_details:
                click.echo("\nTeam Members: None")
            else:
                # Prepare members table
                headers = ["User ID", "Name", "Primary Email", "Primary Phone"]
                table_data = [
                    [
                        member["id"],
                        member["name"],
                        next((email.get("email") for email in member["emails"] if email.get("primary")), "N/A"),
                        next((phone.get("phone") for phone in member["phones"] if phone.get("primary")), "N/A")
                    ]
                    for member in member_details
                ]
                click.echo("\nTeam Members:")
                click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
        
        # Fetch and display team admins
        admins = team.get("admin_account_user_ids", [])
        if not admins:
            click.echo("\nTeam Admins: None")
        else:
            admin_details = []
            for admin_id in admins:
                try:
                    user = client.show_user(admin_id)
                    user_data = user.get("user", {})
                    admin_details.append({
                        "id": user.get("id", "N/A"),
                        "name": user_data.get("name", "N/A"),
                        "emails": user_data.get("emails", []),
                        "phones": user_data.get("phones", [])
                    })
                except Exception as e:
                    click.echo(f"Warning: Could not fetch details for admin {admin_id}: {str(e)}", err=True)
            
            if not admin_details:
                click.echo("\nTeam Admins: None")
            else:
                # Prepare admins table
                headers = ["User ID", "Name", "Primary Email", "Primary Phone"]
                table_data = [
                    [
                        admin["id"],
                        admin["name"],
                        next((email.get("email") for email in admin["emails"] if email.get("primary")), "N/A"),
                        next((phone.get("phone") for phone in admin["phones"] if phone.get("primary")), "N/A")
                    ]
                    for admin in admin_details
                ]
                click.echo("\nTeam Admins:")
                click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
        
    except Exception as e:
        handle_api_error(e, action="showing team")

@teams.command(name="update")
@click.argument("team_id", required=True)
@click.option("--name", help="New name of the team")
@click.option("--notes", help="New notes for the team")
@click.option("--member-id", "member_ids", multiple=True, help="Account user IDs to set as team members")
@click.option("--admin-id", "admin_ids", multiple=True, help="Account user IDs to set as team admins")
@click.pass_context
def update_team_cmd(ctx, team_id, name, notes, member_ids, admin_ids):
    """Update a team in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.update_team(
            team_id=team_id,
            name=name,
            notes=notes,
            member_account_user_ids=list(member_ids) if member_ids else None,
            admin_account_user_ids=list(admin_ids) if admin_ids else None
        )
        click.echo(f"Team updated successfully: {result.get('id', 'N/A')}")
    except Exception as e:
        handle_api_error(e, action="updating team")

@teams.command(name="delete")
@click.argument("team_id", required=True)
@click.option("--force", is_flag=True, help="Delete the team without confirmation")
@click.pass_context
def delete_team_cmd(ctx, team_id, force):
    """Delete a team in PagerTree."""
    if not force and not click.confirm(f"Are you sure you want to delete team {team_id}?"):
        click.echo("Deletion cancelled.")
        return
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.delete_team(team_id)
        click.echo(f"Team deleted successfully: {team_id}")
    except Exception as e:
        handle_api_error(e, action="deleting team")

@teams.command(name="current-oncall")
@click.argument("team_id", required=True)
@click.pass_context
def current_oncall_cmd(ctx, team_id):
    """Show current on-call users for a specific team in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.get_team_current_oncall(team_id)
        if not result:
            click.echo(f"No one schedule oncall for team {team_id}")
            return
        
        # Process each schedule
        for schedule in result:
            layer = schedule.get("layer", "N/A")
            start_time = schedule.get("start_time", "N/A")
            end_time = schedule.get("end_time", "N/A")
            attendees = []
            
            # Fetch user details for each attendee
            for attendee in schedule.get("attendees", []):
                attendee_id = attendee.get("attendee_id")
                if attendee_id:
                    try:
                        user = client.show_user(attendee_id)
                        user_data = user.get("user", {})
                        attendees.append({
                            "id": user.get("id", "N/A"),
                            "name": user_data.get("name", "N/A"),
                            "emails": user_data.get("emails", []),
                            "phones": user_data.get("phones", [])
                        })
                    except Exception as e:
                        click.echo(f"Warning: Could not fetch details for user {attendee_id}: {str(e)}", err=True)
            
            if not attendees:
                click.echo(f"*** LAYER {layer} ({start_time} to {end_time}): No users on-call ***")
                continue
            
            # Prepare table data
            headers = ["User ID", "Name", "Primary Email", "Primary Phone"]
            table_data = [
                [
                    attendee["id"],
                    attendee["name"],
                    next((email.get("email") for email in attendee["emails"] if email.get("primary")), "N/A"),
                    next((phone.get("phone") for phone in attendee["phones"] if phone.get("primary")), "N/A")
                ]
                for attendee in attendees
            ]
            click.echo(f"*** LAYER {layer} ({start_time} to {end_time}): ***")
            click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
            click.echo(f"*** End of layer {layer} ***")
            click.echo("\n")
            
    except Exception as e:
        handle_api_error(e, action="showing current on-call users")

@teams.command(name="alerts")
@click.argument("team_id", required=True)
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of alerts per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.pass_context
def team_alerts_cmd(ctx, team_id, limit, offset):
    """List alerts for a specific team in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.get_team_alerts(team_id, limit=limit, offset=offset)
        alerts_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Title", "Status"]
        table_data = [
            [alert.get("id"), alert.get("title", "N/A"), alert.get("status", "N/A")]
            for alert in alerts_list
        ]
        display_paginated_results(alerts_list, total, limit, offset, "alert", headers, table_data)
    except Exception as e:
        handle_api_error(e, action="listing team alerts")