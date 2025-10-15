"""
Pytest 配置文件
定义测试夹具和全局配置
"""
import pytest
from playwright.async_api import async_playwright
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def browser():
    """浏览器会话级夹具"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture(scope="function")
async def page(browser):
    """页面函数级夹具"""
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()

@pytest.fixture(scope="function")
async def page_with_viewport(browser):
    """带自定义视口的页面夹具"""
    context = await browser.new_context(viewport={"width": 1280, "height": 720})
    page = await context.new_page()
    yield page
    await context.close()

