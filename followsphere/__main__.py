import typer
from beaupy import select
from rich.console import Console

from followsphere.linkedin import execute_linkedin
from followsphere.utils import install_playwright_browsers, show_banner


def main():
    console = Console()
    console.clear()
    install_playwright_browsers()
    show_banner()
    names = [
        "Linkedin",
        "Instagram (Coming soon)",
    ]
    console.print("Choose your platform")
    name: str = select(sorted(names), cursor="🢧", cursor_style="red")
    if name.lower() == "linkedin":
        typer.run(execute_linkedin)
    else:
        typer.echo("\nInvalid platform selected.")


if __name__ == "__main__":
    typer.run(main)
