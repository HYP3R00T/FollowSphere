from typing import List

import typer
from beaupy import select
from rich.console import Console

from followsphere.linkedin import execute_linkedin
from followsphere.utils import install_playwright_browsers, show_banner


def main():
    console: Console = Console()
    console.clear()
    install_playwright_browsers()
    show_banner()
    options: List[str] = [
        "Linkedin",
        "Instagram (Coming soon)",
    ]
    console.print("Pick a platform (Use arrow keys)\n", style="Cyan")
    option: str = select(sorted(options), cursor="\uf061", cursor_style="red")
    if option.lower() == "linkedin":
        typer.run(execute_linkedin)
    else:
        typer.echo("\nInvalid platform selected.")


if __name__ == "__main__":
    typer.run(main)
