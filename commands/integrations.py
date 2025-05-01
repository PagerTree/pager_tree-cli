import click
import json
from utils import display_paginated_results, handle_api_error, format_item_details

@click.group()
def integrations():
    """Commands for managing PagerTree integrations."""
    pass

@integrations.command(name="show")
@click.argument("integration_id", required=True)
@click.pass_context
def show_integration_cmd(ctx, integration_id):
    """Show details of a specific integration in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        integration = client.show_integration(integration_id)
        fields = {
            "id": "ID",
            "name": "Name",
            "integration_type.name": "Type",
            "enabled": "Enabled",
            "created_at": "Created At",
            "updated_at": "Updated At"
        }
        format_item_details(integration, fields)
    except Exception as e:
        handle_api_error(e, "showing integration")

@integrations.command(name="list")
@click.option("--limit", default=10, type=click.IntRange(1, 100), help="Number of integrations per page")
@click.option("--offset", default=0, type=click.IntRange(0), help="Starting point for pagination")
@click.option("--search", help="Search for integrations by name or type")
@click.option("--enabled", is_flag=True, help="Filter for enabled integrations", default=None)
@click.option("--disabled", is_flag=True, help="Filter for disabled integrations")
@click.pass_context
def list_integrations_cmd(ctx, limit, offset, search, enabled, disabled):
    """List integrations in PagerTree with pagination."""
    try:
        # Ensure --enabled and --disabled are mutually exclusive
        if enabled and disabled:
            click.echo("Error: --enabled and --disabled cannot be used together.")
            return

        # Set enabled parameter: True for --enabled, False for --disabled, None if neither
        enabled_param = 1 if enabled else 0 if disabled else None

        client = ctx.obj.client  # Get PagerTreeClient from context
        logger = ctx.obj.logger  # Get logger from context
        logger.debug(f"Listing integrations with limit={limit}, offset={offset}, search={search}, enabled={enabled_param}")
        result = client.list_integrations(limit=limit, offset=offset, search=search, enabled=enabled_param)
        logger.debug(f"Full response: {json.dumps(result, indent=2)}")
        integrations_list = result["data"]
        total = result["total"]
        # Prepare table data
        headers = ["ID", "Name", "Type", "Enabled"]
        table_data = [[integration.get("id"), integration.get("name"), integration.get("integration_type").get("name"), integration.get("enabled")] for integration in integrations_list]
        display_paginated_results(integrations_list, total, limit, offset, "integration", headers, table_data)
    except Exception as e:
        logger.error(f"Error listing integrations: {str(e)}")
        handle_api_error(e, action="listing integrations")

@integrations.command(name="enable")
@click.argument("integration_id", required=True)
@click.pass_context
def enable_integration_cmd(ctx, integration_id):
    """Enable an integration in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.update_integration(integration_id, enabled=True)
        click.echo(f"Integration enabled successfully: {result.get('id')}")
    except Exception as e:
        handle_api_error(e, action="enabling integration")

@integrations.command(name="disable")
@click.argument("integration_id", required=True)
@click.pass_context
def disable_integration_cmd(ctx, integration_id):
    """Disable an integration in PagerTree."""
    try:
        client = ctx.obj.client  # Get PagerTreeClient from context
        result = client.update_integration(integration_id, enabled=False)
        click.echo(f"Integration disabled successfully: {result.get('id')}")
    except Exception as e:
        handle_api_error(e, action="disabling integration")