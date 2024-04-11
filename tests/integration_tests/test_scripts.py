import os
import subprocess

from fixtures import (  # noqa: F401
    cognito_client_id,
    cognito_region,
    password,
    random_file_path,
    revoize_url,
    test_file_path,
    username,
)


def test_enhance_cli(
    password,
    random_file_path,
    test_file_path,
    username,
    revoize_url,
    cognito_client_id,
    cognito_region,  # noqa: F811
):
    # TODO: improve this test handling. The point is that we want to separately test
    # for cases where we supply the revoize-url and cognito-* parameters and for
    # cases where we don't. Currently this is handled by executing the tests twice
    # with different configurations.

    if revoize_url is None and cognito_client_id is None and cognito_region is None:
        subprocess.run(
            [
                "poetry",
                "run",
                "revoize-enhance",
                "--username",
                username,
                "--password",
                password,
                "--input-file-path",
                test_file_path,
                "--output-file-path",
                random_file_path,
            ]
        )
        assert os.path.isfile(random_file_path)
        # Check file has at least 250kb, the actual file will have over 700 kb
        # but this can depend on various factors and we don't want this to be too
        # sensitive
        assert os.path.getsize(random_file_path) > 250_000
    else:
        # Test that the enhance CLI tool works properly
        subprocess.run(
            [
                "poetry",
                "run",
                "revoize-enhance",
                "--username",
                username,
                "--password",
                password,
                "--revoize-url",
                revoize_url,
                "--input-file-path",
                test_file_path,
                "--output-file-path",
                random_file_path,
                "--cognito-client-id",
                cognito_client_id,
                "--cognito-region",
                cognito_region,
            ]
        )
        assert os.path.isfile(random_file_path)
        # Check file has at least 250kb, the actual file will have over 700 kb
        # but this can depend on various factors and we don't want this to be too
        # sensitive
        assert os.path.getsize(random_file_path) > 250_000
