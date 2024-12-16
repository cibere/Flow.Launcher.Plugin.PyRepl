from flogin import Settings

class PyReplSettings(Settings):
    site_packages_path: str | None
    env_json: str | None
    just_show_me_the_tb: bool
    executable: str | None