import click
from utils import display_paginated_results, handle_api_error, format_item_details

@click.group()
def users():
    """Commands for managing PagerTree users."""
    pass

@users.command(name="create")
@click.option("--name", required=True, help="Full name of the user")
@click.option("--email", required=True, help="Email address of the user")
@click.option("--role", type=click.Choice(["admin", "billing", "broadcaster", "communicator"]), multiple=True, help="Roles for the user (can specify multiple)")
@click.option("--team-id", "team_ids", multiple=True, help="IDs of teams the user should be assigned to")
@click.pass_context
def create_user_cmd(ctx, name, email, role, team_ids):
    """Create a new account user in PagerTree."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        roles = {r: True for r in role} if role else {}
        result = client.create_user(name=name, email=email, roles=roles, team_ids=list(team_ids))
        click.echo(f"User created successfully: {result.get('tiny_id')}")
    except Exception as e:
        handle_api_error(e, action="creating user")

@users.command(name="list")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of users per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.pass_context
def list_users_cmd(ctx, limit, offset):
    """List users in PagerTree with pagination."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        result = client.list_users(limit=limit, offset=offset)
        users_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Name", "Primary Email", "Primary Phone", "Roles"]
        table_data = [
            [
                user.get("tiny_id"),
                user.get("user", {}).get("name", "N/A"),
                next((email.get("email") for email in user.get("user", {}).get("emails", []) if email.get("primary")), "N/A"),
                next((phone.get("phone") for phone in user.get("user", {}).get("phones", []) if phone.get("primary")), "N/A"),
                ", ".join(
                    role for role, enabled in user.get("roles", {}).items() if enabled
                ) or "None"
            ]
            for user in users_list
        ]
        display_paginated_results(users_list, total, limit, offset, "user", headers, table_data)
    except Exception as e:
        handle_api_error(e, action="listing users")

@users.command(name="show")
@click.argument("user_id", required=True)
@click.pass_context
def show_user_cmd(ctx, user_id):
    """Show details of a specific user in PagerTree."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        user = client.show_user(user_id)
        fields = {
            "user.id": "User ID",
            "user.name": "Name",
            "user.emails.primary": "Primary Email",
            "user.phones.primary": "Primary Phone",
            "roles": "Roles",
            "created_at": "Created At"
        }
        formatted_user = {
            "user.id": user.get("tiny_id"),
            "user.name": user.get("user", {}).get("name", "N/A"),
            "user.emails.primary": next(
                (email.get("email") for email in user.get("user", {}).get("emails", []) if email.get("primary")),
                "N/A"
            ),
            "user.phones.primary": next(
                (phone.get("phone") for phone in user.get("user", {}).get("phones", []) if phone.get("primary")),
                "N/A"
            ),
            "roles": ", ".join(
                role for role, enabled in user.get("roles", {}).items() if enabled
            ) or "None",
            "created_at": user.get("created_at", "N/A")
        }
        format_item_details(formatted_user, fields)
    except Exception as e:
        handle_api_error(e, action="showing user")

@users.command(name="update")
@click.argument("user_id", required=True)
@click.option("--name", help="New full name of the user")
@click.pass_context
def update_user_cmd(ctx, user_id, name):
    """Update an account user in PagerTree."""
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        result = client.update_user(user_id=user_id, name=name)
        click.echo(f"User updated successfully: {result.get('tiny_id')}")
    except Exception as e:
        handle_api_error(e, action="updating user")

@users.command(name="delete")
@click.argument("user_id", required=True)
@click.option("--force", is_flag=True, help="Delete the user without confirmation")
@click.pass_context
def delete_user_cmd(ctx, user_id, force):
    """Delete a user in PagerTree."""
    if not force and not click.confirm(f"Are you sure you want to delete user {user_id}?"):
        click.echo("Deletion cancelled.")
        return
    try:
        client = ctx.obj  # Get PagerTreeClient from context
        result = client.delete_user(user_id)
        click.echo(f"User deleted successfully: {user_id}")
    except Exception as e:
        handle_api_error(e, action="deleting user")