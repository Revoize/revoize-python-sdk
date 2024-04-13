import os
import uuid
from typing import Generator, Optional

import pytest

from revoize.auth import login
from revoize.schema import Credentials


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    username = load_env_var("TEST_USERNAME")
    password = load_env_var("TEST_PASSWORD")
    cognito_client_id = load_env_var("COGNITO_CLIENT_ID")
    cognito_region = load_env_var("COGNITO_REGION")
    return login(username, password, cognito_client_id, cognito_region)


@pytest.fixture(scope="session")
def username() -> str:
    return load_env_var("TEST_USERNAME")


@pytest.fixture(scope="session")
def password() -> str:
    return load_env_var("TEST_PASSWORD")


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
def cognito_client_id() -> Optional[str]:
    return load_env_var_or_none("COGNITO_CLIENT_ID")


@pytest.fixture(scope="session")
def cognito_region() -> Optional[str]:
    return load_env_var_or_none("COGNITO_REGION")


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
