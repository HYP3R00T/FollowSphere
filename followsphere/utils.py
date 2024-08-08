import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Union

from beaupy import select_multiple
from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from termcolor import cprint


def install_playwright_browsers() -> None:
    console: Console = Console()
    try:
        from playwright.sync_api import Browser, sync_playwright

        with sync_playwright() as p:
            browser: Browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("Playwright browsers installed successfully.")
    console.clear()


def show_banner() -> None:
    try:
        width: int = os.get_terminal_size()[0]
    except Exception:
        width = 80

    banner: Figlet = Figlet(font="big", justify="center", width=width)
    cprint(banner.renderText("FollowSphere"), color="blue")

    url: str = "https://hyperoot.dev"
    console: Console = Console()
    console.print(Panel(f"{url}"), justify="center", style="green")


def show_goodbye() -> None:
    console: Console = Console()
    console.clear()
    message: str = """
Thanks for using [blue]FollowSphere[/blue]\n
You can follow me at [blue]https://www.linkedin.com/in/rajesh-kumar-das/[/blue]\n
Source code is available at [blue]https://github.com/HYP3R00T/FollowSphere[/blue]
        """
    console.print(Panel(message, title="[red]\uf004 Thank you \uf004[/red]", border_style="red"), justify="center")


def read_data() -> Optional[Dict]:
    try:
        script_dir: str = os.path.dirname(os.path.abspath(__file__))
        data_file_path: str = os.path.join(script_dir, "data.json")
        with open(data_file_path, "r") as file:
            data: Dict = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found")
        exit()


def tags_follower(data: Dict[str, Any]) -> Optional[List[str]]:
    console: Console = Console()
    console.clear()
    show_banner()
    options: List[str] = []
    for k, _v in data.items():
        options.append(k)

    console.print("Which tag collection do you want to follow?\n", style="Cyan")
    items: List[Union[int, Any]] = select_multiple(
        sorted(options), tick_character="✓", ticked_indices=None, tick_style="green"
    )
    if items:
        console.print(f"\nSelected tag collections: [green]{" ".join(items)}[/green]")
        tags: List[str] = []
        for item in items:
            if data[item]["tags"]:
                for tag in data[item]["tags"]:
                    if tag not in tags:
                        tags.append(tag)
        return tags
    else:
        console.print("You didn't select anything. Terminating the program.")
        exit()
