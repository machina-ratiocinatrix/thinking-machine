import subprocess
import pytest
import os

def test_uvx_integration():
    """
    Tests the library fully end-to-end through `uvx` by installing from the local
    directory (--from .), simulating exactly how a user would interact with the
    script once it is deployed to PyPI.
    """
    
    # We know the environment variables are already in the computer
    # So we don't need to mock them; we just execute the real thing.
    
    input_text = "Theodotos-Alexandreus: Are language models seeking the Truth, machine?\n"
    
    # "uvx --from . name-of-the-machine" behaves identically to PyPI "uvx name-of-the-machine"
    cmd = [
        "uvx", 
        "--with",
        ".[all]",
        "--from", 
        ".", 
        "name-of-the-machine"
    ]
    
    # The keys/tokens are passed through the environment automatically via env=env.
    # We don't pass them as CLI arguments because `fileinput.input()` in cli.py 
    # would try to read them as files.

    print(f"Running command: {' '.join(cmd)}")
    
    env = os.environ.copy()
    result = subprocess.run(cmd, input=input_text, text=True, capture_output=True, env=env)
    
    # We expect a successful execution (0)
    assert result.returncode == 0, f"Process failed with stderr:\n{result.stderr}\n\nstdout:\n{result.stdout}"
    
    # The output should contain our original input
    assert "Theodotos-Alexandreus:" in result.stdout
    assert "Are language models seeking the Truth, machine?" in result.stdout
    
    # The Machine string should be present, indicating it replied back and added to the transcript
    # (Since it is appending it to the bottom, the stdout length > input length)
    assert len(result.stdout) > len(input_text), "The machine did not append any response."
