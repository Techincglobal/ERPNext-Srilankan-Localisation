import click

from erpnext_srilankan_localisation.setup import before_uninstall as remove_setup


def before_uninstall():
    try:
        print("Removing customizations created by ERPNext Sri Lankan Localisation...")
        remove_setup()

    except Exception as e:
        click.secho(
            "Removing ERPNext Sri Lankan Localisation customizations failed due to an error. "
            "Please try again.",
            fg="bright_red",
        )
        raise e

    click.secho(
        "ERPNext Sri Lankan Localisation customizations have been removed successfully...",
        fg="green",
    )