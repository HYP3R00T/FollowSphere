import json
import os
import subprocess
import sys
from typing import Dict, List, Optional

from beaupy import select_multiple
from rich.console import Console


def install_playwright_browsers():
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("Playwright browsers installed successfully.")


def read_data() -> Optional[Dict]:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(script_dir, "data.json")
        with open(data_file_path, "r") as file:
            data: Dict = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found")
        exit()


def tags_follower(data: Dict):
    console = Console()
    options: List = []
    for k, _v in data.items():
        options.append(k)

    console.print("Which tag collection do you want to follow?")
    items = select_multiple(options, tick_character="🎒", ticked_indices=[0])
    console.print(f"You selected {items}")
    tags = []
    for item in items:
        if data[item]["tags"]:
            for tag in data[item]["tags"]:
                if tag not in tags:
                    tags.append(tag)
    return tags
