import sys, subprocess, os, logging, io

CODE_TEMPLATE = """
import os, sys

for path in {PACKAGE_PATH_LIST}:
    sys.path.append(path)

import import_expression
code = {CODE}
import_expression.eval(code)
"""

LOG = logging.getLogger(__name__)

def execute_code(body: str, executable: str | None = None, package_paths: list[str] | None = None) -> tuple[str, str]:
    executable = executable or sys.executable
    package_paths = package_paths or []

    parent_folder_path = os.path.abspath(os.path.dirname(__file__))
    package_paths.append(os.path.join(parent_folder_path, "exe-libs"))

    code = CODE_TEMPLATE.format(PACKAGE_PATH_LIST=str(package_paths), CODE=repr(body))
    cmd = [executable, "-c", body] #code]

    LOG.debug(f"Executing code. cmd: {cmd!r}")

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.wait(5)

    LOG.debug(f"Code has finished processing. proc: {proc!r}")

    assert proc.stderr
    assert proc.stdout

    return proc.stderr.read().decode().strip(), proc.stdout.read().decode().strip()