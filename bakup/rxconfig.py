import reflex as rx
import os
import shutil
import subprocess

# Define the configuration for the Reflex app
config = rx.Config(
    app_name="pip install",
    plugins=[rx.plugins.TailwindV3Plugin()],
)

# Change directory to the app's root folder
os.chdir("WoldVirtual.0.0.1")

# Clean up previous builds and caches
shutil.rmtree(".web", ignore_errors=True)
shutil.rmtree("__pycache__", ignore_errors=True)

# Run the application
subprocess.run(["python", "WoldVirtual_Crypto_3Dv1.py"])