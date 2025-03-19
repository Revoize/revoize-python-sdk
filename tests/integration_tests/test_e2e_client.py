import os

from fixtures import api_key, random_file_path, test_file_path  # noqa: F401

from revoize import RevoizeClient


def test_client(
    api_key,  # noqa: F811
    random_file_path,  # noqa: F811
    test_file_path,  # noqa: F811
):
    client = RevoizeClient(api_key)
    client.enhance_file(test_file_path, random_file_path)
    assert os.path.isfile(random_file_path)
    # Check file has at least 250 kb, the actual file will have over 700 kb
    # but this can depend on various factors and we don't want this to be too
    # sensitive
    assert os.path.getsize(random_file_path) > 250_000


def test_get_all_enhancements(api_key):  # noqa: F811
    # This test assumes there were already enhancements created for this account
    # Which means this may fail the first time it's executed
    client = RevoizeClient(api_key)
    enhancements = client.get_all_enhancements()
    assert isinstance(enhancements, list)
    assert len(enhancements) >= 1
