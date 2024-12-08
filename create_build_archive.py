import zipfile, click

FILES = ("plugin.json", "main.exe", "icon.png", "SettingsTemplate.yaml")

@click.command()
@click.argument("name")
def create_archive(name: str):
    with zipfile.ZipFile(name, "w") as zf:
        for file in FILES:
            zf.write(file)
            print(f"Added {file}")

if __name__ == "__main__":
    create_archive()