import typer

from followsphere.linkedin import execute_linkedin
from followsphere.utils import install_playwright_browsers

if __name__ == "__main__":
    install_playwright_browsers()
    typer.run(execute_linkedin)
