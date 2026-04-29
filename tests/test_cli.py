import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from name_of_the_machine.cli import run

@patch('name_of_the_machine.cli.fileinput')
@patch('name_of_the_machine.machine.machine')
def test_cli_run_success(mock_machine, mock_fileinput):
    # Mocking standard input pipeline
    mock_fileinput.input.return_value = ["user: hello\n"]
    mock_machine.return_value = ("some thoughts", "response text")
    
    runner = CliRunner()
    result = runner.invoke(run, ['--provider-api-key', 'sk-ant-test'])
    
    # We exit cleanly when normal things happen. Wait, sys.stdout.write is called but
    # click catches SystemExit(0).
    # Since click catches exceptions, we just verify the mock is called
    assert mock_machine.called, f"Output: {result.output}\nException: {result.exception}"
    assert "response text" in result.output
