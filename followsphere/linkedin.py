import asyncio
from typing import Dict, List

import typer
from playwright.async_api import Browser, ElementHandle, Page, async_playwright
from typing_extensions import Annotated

from followsphere.utils import read_data, tags_follower


async def login(page: Page, username: str, password: str):
    await page.goto("https://www.linkedin.com/login")
    await page.fill("input#username", username)
    await page.fill("input#password", password)
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")


async def follow_hashtags(page: Page, hashtags: List[str]):
    for hashtag in hashtags:
        try:
            await page.goto(f"https://www.linkedin.com/feed/hashtag/{hashtag.lower()}/")
            follow_button: ElementHandle = await page.query_selector("button.follow")
            if follow_button:
                # Check if the button has the 'is-following' class
                class_name = await follow_button.get_attribute("class")
                if "is-following" in class_name:
                    print(f"Already following #{hashtag}.")
                else:
                    # Click the follow button if it's not followed yet
                    await follow_button.click()
                    print(f"Clicked follow for #{hashtag}.")
        except Exception as e:
            print(f"An error occurred for #{hashtag}: {e}")


async def entrypoint(linkedin_username: str, linkedin_password: str, hashtags: List[str]):
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=False)  # Set to False to see the browser in action
        page: Page = await browser.new_page()
        await login(page, linkedin_username, linkedin_password)
        await follow_hashtags(page, hashtags)
        await browser.close()


def execute_linkedin(
    username: Annotated[str, typer.Option(prompt="Enter your username or email")],
    password: Annotated[str, typer.Option(prompt="Enter your password", hide_input=True, confirmation_prompt=True)],
):
    data: Dict = read_data()["LinkedIn"]
    print(data)
    hashtags: List[str] = tags_follower(data)
    asyncio.run(entrypoint(username, password, hashtags))
