from typing import Annotated, List, Optional

import typer
from beaupy import select
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from followsphere.linkedin import execute_linkedin, execute_unfollow_linkedin
from followsphere.utils import install_playwright_browsers, show_banner, show_goodbye


def main(
    follow: Annotated[Optional[bool], typer.Option(help="Activate unfollow mode")] = True,
    force: Annotated[Optional[bool], typer.Option(help="Skip the warning message")] = False,
):
    console: Console = Console()
    console.clear()
    show_banner()
    console.print(
        Panel(
            "\nThis action will make permanent changes to your selected platforms. These changes cannot be undone. Proceed with caution.\n",
            title="\uee15 Warning \uee15",
            border_style="red",
        ),
        style="yellow",
    )
    response: bool = Confirm.ask("Do you want to proceed?", default=False)
    if force or response:
        install_playwright_browsers()
        show_banner()
        print(follow)
        if not follow:
            options: List[str] = [
                "Linkedin",
                "Instagram (Coming soon)",
            ]
            console.print("Select a platform (Use arrow keys)\n", style="Cyan")
            option: str = select(sorted(options), cursor="\uf061", cursor_style="red")
            if option.lower() == "linkedin":
                execute_unfollow_linkedin()
            else:
                print("\nInvalid platform selected.")
        else:
            options: List[str] = [
                "Linkedin",
                "Instagram (Coming soon)",
            ]
            console.print("Select a platform (Use arrow keys)\n", style="Cyan")
            option: str = select(sorted(options), cursor="\uf061", cursor_style="red")
            if option.lower() == "linkedin":
                execute_linkedin()
            else:
                print("\nInvalid platform selected.")
        show_goodbye()


if __name__ == "__main__":
    typer.run(main)
