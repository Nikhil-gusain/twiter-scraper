import os
import re
import pathlib

def generate_requirements_from_venv(venv_path: str, output_file: str = "requirements.txt"):
    """
    Reads installed packages from the .venv directory and writes a requirements.txt manually.
    
    Args:
        venv_path (str): Path to the `.venv` directory.
        output_file (str): Output path for the requirements.txt file.
    """

    site_packages = None

    # Try to find site-packages directory
    for root, dirs, files in os.walk(os.path.join(venv_path, "lib")):
        for dir_name in dirs:
            if dir_name.startswith("python") and "site-packages" in os.listdir(os.path.join(root, dir_name)):
                site_packages = os.path.join(root, dir_name, "site-packages")
                break
        if site_packages:
            break

    if not site_packages:
        raise RuntimeError("Could not find site-packages inside the virtual environment.")

    requirements = []

    for item in os.listdir(site_packages):
        if item.endswith(".dist-info"):
            pkg_name_version = item.replace(".dist-info", "")
            # Split on the last '-' to separate version from name (handles dashes in names)
            if '-' in pkg_name_version:
                parts = pkg_name_version.rsplit("-", 1)
                if len(parts) == 2:
                    pkg, version = parts
                    requirements.append(f"{pkg}=={version}")

    # Sort and write to file
    requirements = sorted(set(requirements))

    with open(output_file, "w") as f:
        f.write("\n".join(requirements))

    print(f"✅ requirements.txt written with {len(requirements)} packages.")

generate_requirements_from_venv(".venv")