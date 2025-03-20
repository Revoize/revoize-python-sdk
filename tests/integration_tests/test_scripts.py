import os
import subprocess

from fixtures import api_key, random_file_path, test_file_path


def test_enhance_cli(api_key, random_file_path, test_file_path):
    subprocess.run(
        [
            "poetry",
            "run",
            "revoize-enhance",
            "--api-key",
            api_key,
            "--input-file-path",
            test_file_path,
            "--output-file-path",
            random_file_path,
        ]
    )
    assert os.path.isfile(random_file_path)
    # Check file has at least 250 kb, the actual file will have over 700 kb
    # but this can depend on various factors and we don't want this to be too
    # sensitive
    assert os.path.getsize(random_file_path) > 250_000
