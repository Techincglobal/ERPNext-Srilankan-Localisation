import click

from erpnext_srilankan_localisation.setup import after_install as setup


def after_install():
    try:
        print("Setting up ERPNext Sri Lankan Localisation...")
        setup()

        click.secho(
            "Thank you for installing ERPNext Sri Lankan Localisation!",
            fg="green",
        )

    except Exception as e:
        click.secho(
            "Installation for ERPNext Sri Lankan Localisation failed due to an error. "
            "Please try re-installing the app.",
            fg="bright_red",
        )
        raise e