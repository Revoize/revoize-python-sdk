import os
import uuid
from typing import Generator, Optional

import pytest


@pytest.fixture(scope="session")
def api_key() -> str:
    return load_env_var("TEST_API_KEY")


@pytest.fixture
def random_file_path() -> Generator[str, None, None]:
    random_file_name = f"./tests/test_data/{str(uuid.uuid4())}"
    yield random_file_name
    try:
        os.remove(random_file_name)
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def revoize_url() -> Optional[str]:
    return load_env_var_or_none("TEST_REVOIZE_URL")


@pytest.fixture(scope="session")
def test_file_path() -> str:
    return "./tests/test_data/test-recording.wav"


def load_env_var(env_var_name: str) -> str:
    value = os.getenv(env_var_name)
    assert isinstance(
        value, str
    ), f"'{env_var_name}' env variable needs to be configured"
    return value


def load_env_var_or_default(env_var_name: str, default: str) -> str:
    return os.getenv(env_var_name, default)


def load_env_var_or_none(env_var_name: str) -> Optional[str]:
    return os.getenv(env_var_name)
