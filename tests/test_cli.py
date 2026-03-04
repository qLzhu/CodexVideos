import subprocess


def test_cli_help_smoke():
    result = subprocess.run(["python", "-m", "app.cli", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "CodexVideos CLI" in result.stdout
