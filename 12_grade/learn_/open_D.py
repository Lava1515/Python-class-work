import os


# Use os.system to open the directory in the default file explorer
os.system(f'explorer "{new_directory_path}"')  # For Windows
# On Linux, you can use 'nautilus' or 'xdg-open' instead of 'explorer'
# On macOS, you can use 'open'