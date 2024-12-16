import zipfile
from pathlib import Path
import click

FILES = ("plugin.json", "main.py", "icon.png", "SettingsTemplate.yaml", "error.png", "plugin/settings.py", "plugin/results.py", "plugin/repl_result.py", "plugin/plugin.py", "plugin/handler.py", "plugin/core.py")


@click.command()
@click.argument("name")
def create_archive(name: str):
    if not name.endswith(".zip"):
        name = f"{name}.zip"
        
    with zipfile.ZipFile(name, "w") as zf:
        for file in FILES:
            zf.write(file)
            print(f"Added {file}")
        
        dir = Path("dist") / "pyrepl_error_ui"
        for root, _, files in dir.walk():
            for file in files:
                zf.write(root / file)
                print(f"Added {file}")


if __name__ == "__main__":
    create_archive()
