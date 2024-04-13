import os
from typing import Optional

import click

from revoize import RevoizeClient
from revoize.schema import EnhancementParameters


@click.command()
@click.option("--username", "-u", help="Your Revoize username", required=True)
@click.option("--password", "-p", help="Your Revoize password", required=True)
@click.option(
    "--input-file-path", "-f", help="Path to file to be enhanced", required=True
)
@click.option("--output-file-path", "-o", help="Output file path")
@click.option(
    "--output-loudness",
    "-l",
    default=-18,
    type=click.IntRange(-32, -8),
    help="Output loudness",
)
@click.option("--revoize-url", help="Revoize URL")
@click.option("--cognito-client-id", help="Cognito Client ID")
@click.option("--cognito-region", help="Cognito Region")
def _enhance(
    username,
    password,
    input_file_path,
    output_file_path,
    output_loudness,
    revoize_url: Optional[str] = None,
    cognito_client_id: Optional[str] = None,
    cognito_region: Optional[str] = None,
):
    """Enhance selected file."""
    if output_file_path is None:
        filename, extension = os.path.splitext(input_file_path)
        output_file_path = f"{filename}-enhanced{extension}"
    client = RevoizeClient(
        username, password, revoize_url, cognito_client_id, cognito_region
    )
    params = EnhancementParameters(loudness=output_loudness)
    client.enhance_file(input_file_path, output_file_path, params)


if __name__ == "__main__":
    _enhance()
