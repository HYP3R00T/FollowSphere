import asyncio
from typing import Any, Dict, List

from beaupy import select
from playwright.async_api import Browser, ElementHandle, Page, async_playwright
from rich.console import Console

from followsphere.utils import read_data, show_banner, tags_follower


async def login(page: Page) -> None:
    await page.goto("https://www.linkedin.com/login")
    await page.wait_for_selector(".authentication-outlet")


async def follow_hashtags(page: Page, hashtags: List[str]) -> None:
    for hashtag in hashtags:
        try:
            await page.goto(f"https://www.linkedin.com/feed/hashtag/{hashtag.lower()}/")
            follow_button: ElementHandle = await page.query_selector("button.follow")
            if follow_button:
                # Check if the button has the 'is-following' class
                class_name: str = await follow_button.get_attribute("class")
                if "is-following" in class_name:
                    print(f"Already following #{hashtag}")
                else:
                    # Click the follow button if it's not followed yet
                    await follow_button.click()
                    print(f"Clicked follow for [green]#{hashtag}[/green]")
        except Exception as e:
            print(f"An error occurred for #{hashtag}: {e}")


async def entrypoint(hashtags: List[str]) -> None:
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=False)  # Set to False to see the browser in action
        page: Page = await browser.new_page()
        await login(page)
        await follow_hashtags(page, hashtags)
        await browser.close()


def execute_linkedin() -> None:
    console: Console = Console()
    console.clear()
    show_banner()
    data: Dict[str, Any] = read_data()["LinkedIn"]
    options: List = []
    for k, _v in data.items():
        options.append(k)
    console.print("Choose your collection (Use arrow keys)\n", style="Cyan")
    option: str = select(sorted(options), cursor="\uf061", cursor_style="red")
    if option == "Role based Collections":
        hashtags: List[str] = tags_follower(data["Role based Collections"])
        asyncio.run(entrypoint(hashtags))
    elif option == "Skill based Collections":
        hashtags: List[str] = tags_follower(data["Skill based Collections"])
        asyncio.run(entrypoint(hashtags))
    else:
        print("\nInvalid option selected")
