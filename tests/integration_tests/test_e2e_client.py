import os

from fixtures import (  # noqa: F401
    cognito_client_id,
    cognito_region,
    password,
    random_file_path,
    revoize_url,
    test_file_path,
    username,
)

from revoize import RevoizeClient


def test_client(
    username,
    password,
    random_file_path,
    test_file_path,
    revoize_url,
    cognito_client_id,
    cognito_region,  # noqa: F811
):
    client = RevoizeClient(
        username,
        password,
        revoize_url=revoize_url,
        cognito_client_id=cognito_client_id,
        cognito_region=cognito_region,
    )
    client.enhance_file(test_file_path, random_file_path)
    assert os.path.isfile(random_file_path)
    # Check file has at least 250kb, the actual file will have over 700 kb
    # but this can depend on various factors and we don't want this to be too
    # sensitive
    assert os.path.getsize(random_file_path) > 250_000


def test_get_all_enhancements(
    username, password, revoize_url, cognito_client_id, cognito_region  # noqa: F811
):
    # This test assumes there were already enhancements created for this account
    # Which means this may fail the first time it's executed
    client = RevoizeClient(
        username,
        password,
        revoize_url=revoize_url,
        cognito_client_id=cognito_client_id,
        cognito_region=cognito_region,
    )
    enhancements = client.get_all_enhancements()
    assert isinstance(enhancements, list)
    assert len(enhancements) >= 1
