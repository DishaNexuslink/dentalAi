import os

# Define folder paths
folders = [
    "app"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)


# Placeholder files for templates, outputs, and app
placeholder_files = {
    "app": [
        "__init__.py",
        "main.py",
        "text_to_json.py",
        "json_to_template.py",
    ]
}

# Create empty placeholder files
for folder, files in placeholder_files.items():
    for file_name in files:
        with open(os.path.join(folder, file_name), 'w') as f:
            pass

print("✅ Folder structure and files created successfully.")
