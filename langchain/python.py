"""Mock Python REPL."""
import sys
from io import StringIO
from typing import Dict, Optional

from pydantic import BaseModel, Field


class PythonREPL(BaseModel):
    """Simulates a standalone Python REPL."""

    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")

    def run(self, command: str) -> str:
        """Run command with own globals/locals and returns anything printed."""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            # exec needs globals == locals
            # see https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec
            exec(command, self.globals, self.globals) # pylint: disable=exec-used
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = str(e)
        return output
