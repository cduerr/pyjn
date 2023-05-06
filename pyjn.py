#!/usr/bin/env python3
import json
import os
import sys

import click

from services.output import warning, error
from services.editor import editor


@click.command()
@click.option("-h", "--help", "help_", is_flag=True, help="Show this help.")
@click.option(
    "-i",
    "--input",
    "input_json",
    default="",
    help="JSON input or filename. STDIN is used if not provided.",
)
@click.option(
    "-e", "--edit", "invoke_editor", is_flag=True, help="Open $EDITOR to edit code."
)
@click.argument("code", required=True, default="")
def pyjn(help_, input_json, invoke_editor, code):
    """
    pyjn -- manipulate json with python
    """
    # Help
    if help_:
        click.echo(click.get_current_context().get_help())
        return

    # Grab Input (file from input_json)
    if input_json and os.path.isfile(input_json):
        with open(input_json, "r") as f:
            input_json = f.read()
    # Grab Input (stdin)
    elif not input_json and not sys.stdin.isatty():
        input_json = sys.stdin.read()
    elif not input_json:
        warning(f"No input. `{sys.argv[0]}` --help for help.")
        return

    # Parse Input
    try:
        data = json.loads(input_json)  # noqa
    except json.decoder.JSONDecodeError:
        error("Invalid JSON.")
        return

    # Invoke Editor
    if invoke_editor:
        code = editor(code)

    # Sanitize Code & Validate
    code = code.strip()
    if not code:
        warning(f"No code. `{sys.argv[0]} --help` for help.")
        return

    # Ensure 'code' is valid Python code:
    try:
        code_object = compile(code, "<string>", "eval")
    except SyntaxError as e:
        error("Syntax error.")
        error(e)
        return
    except Exception as e:
        error("Unknown error compiling code.")
        error(e)
        return

    # Execute the code
    try:
        import jmespath

        result = eval(code_object)
    except Exception as e:
        error("Error executing code.")
        error(e)
        return

    # Output
    try:
        result_str = json.dumps(result)
        print(result_str)
    except Exception as e:
        error("Error serializing result to JSON.")
        error(e)
        return


if __name__ == "__main__":
    # read additional options from env, prepend to cargs
    env_options = os.environ.get("PYJN_OPTIONS", "")
    if env_options:
        sys.argv[1:] = env_options.split() + sys.argv[1:]

    # go
    pyjn()
