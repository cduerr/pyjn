import os
import subprocess
import tempfile


DEFAULT_EDITOR = "vi"


def editor(content: str) -> str:
    """
    Edit a string in the default editor.
    :param content: (str) string to edit
    :return: (str) edited string
    """
    editor = os.environ.get("EDITOR", DEFAULT_EDITOR)
    with tempfile.NamedTemporaryFile(suffix=".tmp", mode="w+") as tf:
        if content:
            tf.write(content)
            tf.flush()
        subprocess.call([editor, tf.name])
        with open(tf.name, "r") as edited_file:
            content = edited_file.read().strip()

    return content
