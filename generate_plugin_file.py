import json

with open("plugin.json", "r") as f:
    data = json.load(f)

data['ID'] = "7ed41d7e3d174379972e1cdacb647474"
data['Name'] = "Worknik Dictionary"
data['Website'] = f"https://github.com/cibere/Flow.Launcher.Plugin.WordNikDictionary/tree/v{data['Version']}"
data['ActionKeyword'] = "def"
data['Language'] = "Executable_v2"
data['ExecuteFileName'] = "pyrepl.exe"

with open("plugin.json", "w") as f:
    json.dump(data, f)

print("New plugin.json contents:")
print(json.dumps(data, indent=4))