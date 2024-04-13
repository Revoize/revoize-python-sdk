# Revoize SDK

[![CI](https://github.com/Revoize/revoize-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/Revoize/revoize-python-sdk/actions/workflows/ci.yml)

This package allows you to interact with [Revoize](https://revoize.com) through Python.

## Installation

To install:

```
pip install revoize
```

## Basic usage

To use this package you will need to have created an account with Revoize and use your account credentials as `username` and `password` in the commands below.

To enhance your file (`my-file.wav`) with Revoize you can either use the CLI:

```bash
revoize-enhance \
    --username **** \
    --password **** \
    --input-file-path my-file.wav \
    --output-file-path my-file-enhanced.wav
```

or through the Python API:

```py
from revoize.api import RevoizeClient

client = RevoizeClient(username="****", password="****")
client.enhance_file("my-file.wav", "my-file-enhanced.wav")
```

## Advanced usage

### Additional parameters

You can also specify some processing parameters:

- output loudness - in LUFS, between -32 and -8

Using the CLI you can specify this through the `--output-loudness` parameter.

Using the Python API:

```py
from revoize.api import RevoizeClient
from revoize.schema import EnhancementParameters

client = RevoizeClient(username="****", password="****")
params = EnhancementParameters(loudness=-20)
client.enhance_file("my-file.wav", "my-file-enhanced.wav", params)
```

### Using with a different Revoize tenant

You may need to use this SDK against a different Revoize environment than our production. In that case, you should be provided 3 configuration parameters:

- `cognito_client_id`
- `cognito_region`
- `revoize_url`

All of those should be passed to the `RevoizeClient` constructor like:

```py
from revoize.api import RevoizeClient
client = RevoizeClient(
    username="****",
    password="****",
    revoize_url=revoize_url,
    cognito_client_id=cognito_client_id,
    cognito_region=cognito_region
)
```

After this setup, you can use the `client` object as usual.

## Publishing to PyPI

This section contains a guide for maintainers about publishing to PyPI.

Before you can publish updates to this package you need to go through a few steps of configuration:

0. Globally install `poetry` (https://python-poetry.org/) and `poethepoet` (https://poethepoet.natn.io/)
1. Create a PyPI account.
2. Contact Revoize admins to add you to package maintainers.
3. Create a PyPI API token.
4. Configure Poetry to use the API token with `poetry config pypi-token.pypi <token>`

You can then issue updates with:

1. `poe bump-version (major|minor|patch)`
2. Commit the change, have it reviewed and merged
3. `poe publish`

## Testing

To test the SDK against production environment, all you need to do is run:

```sh
TEST_USERNAME="<your Revoize username>" TEST_PASSWORD="<your Revoize password>" poe test
```

If you would like to test the SDK against a different environment, you need to supply additional env variables:

```py
TEST_USERNAME="***" \
    TEST_PASSWORD="***" \
    TEST_REVOIZE_URL="***" \
    COGNITO_CLIENT_ID="***" \
    COGNITO_REGION="***"
    poe test
```

Feel free to contact Revoize Support to find out what values you should use here.
