import json

with open("plugin.json", "r") as f:
    data = json.load(f)

data['ID'] = "8d7d2301-4d69-4da2-a19b-e51c8ea239a9"
data['Name'] = "PyRepl"
data['Website'] = f"https://github.com/cibere/Flow.Launcher.Plugin.PyRepl/tree/v{data['Version']}"
data['ActionKeyword'] = "py"
data['Language'] = "executable_v2"
data['ExecuteFileName'] = "main.exe"

with open("plugin.json", "w") as f:
    json.dump(data, f, indent=4)

print("New plugin.json contents:")
print(json.dumps(data, indent=4))