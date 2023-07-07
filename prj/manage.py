import argparse
import importlib
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('app_name', help='Name of the app to run')
    args = parser.parse_args()

    app_name = args.app_name

    if not os.path.exists(f'apps/{app_name}/app.py'):
        print(f"No such app: {app_name}")
        sys.exit(1)

    try:
        app_module = importlib.import_module(f'apps.{app_name}.app')
    except ImportError as e:
        print(f"Error importing app: {e}")
        sys.exit(1)

    try:
        app_module.run()
    except AttributeError:
        print(f"App {app_name} does not have a run function")
        sys.exit(1)

if __name__ == "__main__":
    main()