#!/usr/bin/env python3
"""
Playwright 高级功能演示
包括网络拦截、移动设备模拟、多页面管理等高级特性
"""
import asyncio
import json
from playwright.async_api import async_playwright

async def network_interception_demo():
    """网络拦截演示"""
    print("🌐 网络拦截演示...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 拦截所有网络请求
        intercepted_requests = []
        
        async def handle_request(request):
            intercepted_requests.append({
                "url": request.url,
                "method": request.method,
                "headers": dict(request.headers)
            })
            print(f"🔍 拦截请求: {request.method} {request.url}")
        
        # 设置请求拦截
        page.on("request", handle_request)
        
        # 拦截响应
        async def handle_response(response):
            if "api" in response.url:
                print(f"📡 API响应: {response.status} {response.url}")
        
        page.on("response", handle_response)
        
        await page.goto("https://httpbin.org/")
        await page.wait_for_load_state("networkidle")
        
        print(f"📊 总共拦截了 {len(intercepted_requests)} 个请求")
        
        # 保存拦截的请求信息
        with open("logs/intercepted_requests.json", "w", encoding="utf-8") as f:
            json.dump(intercepted_requests, f, indent=2, ensure_ascii=False)
        
        await browser.close()
        print("✅ 网络拦截演示完成!")

async def mobile_simulation_demo():
    """移动设备模拟演示"""
    print("\n📱 移动设备模拟演示...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # 模拟iPhone 12
        iphone_12 = p.devices["iPhone 12"]
        context = await browser.new_context(**iphone_12)
        page = await context.new_page()
        
        print("📱 模拟 iPhone 12 访问网站...")
        await page.goto("https://m.baidu.com")
        await page.wait_for_load_state("networkidle")
        
        # 获取视口信息
        viewport = page.viewport_size
        print(f"📐 视口大小: {viewport['width']} x {viewport['height']}")
        
        # 截图移动版页面
        await page.screenshot(path="screenshots/mobile_baidu.png")
        print("📸 已保存移动版截图")
        
        # 测试触摸操作
        search_input = page.locator("#index-kw")
        await search_input.tap()  # 使用tap而不是click
        await search_input.fill("移动端测试")
        
        # 模拟滑动操作
        await page.swipe(0, 300, 0, 100)  # 向上滑动
        
        await page.screenshot(path="screenshots/mobile_interaction.png")
        
        await browser.close()
        print("✅ 移动设备模拟演示完成!")

async def multi_page_demo():
    """多页面管理演示"""
    print("\n🗂️  多页面管理演示...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # 创建多个页面
        pages = []
        urls = [
            "https://httpbin.org/",
            "https://httpbin.org/json",
            "https://httpbin.org/html"
        ]
        
        for i, url in enumerate(urls):
            page = await context.new_page()
            pages.append(page)
            await page.goto(url)
            print(f"📄 页面 {i+1} 已加载: {url}")
        
        # 在所有页面上执行操作
        for i, page in enumerate(pages):
            title = await page.title()
            await page.screenshot(path=f"screenshots/page_{i+1}.png")
            print(f"📸 页面 {i+1} 截图已保存, 标题: {title}")
        
        # 页面间切换
        await pages[0].bring_to_front()
        print("🔄 切换到第一个页面")
        
        # 关闭特定页面
        await pages[1].close()
        print("❌ 关闭第二个页面")
        
        await browser.close()
        print("✅ 多页面管理演示完成!")

async def javascript_execution_demo():
    """JavaScript执行演示"""
    print("\n🔧 JavaScript执行演示...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto("https://httpbin.org/")
        
        # 执行JavaScript获取页面信息
        page_info = await page.evaluate("""
            () => {
                return {
                    url: window.location.href,
                    title: document.title,
                    userAgent: navigator.userAgent,
                    windowSize: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    linksCount: document.querySelectorAll('a').length
                };
            }
        """)
        
        print("📊 页面信息:")
        for key, value in page_info.items():
            print(f"  {key}: {value}")
        
        # 修改页面内容
        await page.evaluate("""
            () => {
                const header = document.querySelector('h1');
                if (header) {
                    header.style.color = 'red';
                    header.textContent = 'Playwright 修改了这个标题!';
                }
            }
        """)
        
        await page.screenshot(path="screenshots/js_modified.png")
        print("📸 JavaScript修改后的页面截图已保存")
        
        await browser.close()
        print("✅ JavaScript执行演示完成!")

async def wait_strategies_demo():
    """等待策略演示"""
    print("\n⏳ 等待策略演示...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto("https://httpbin.org/delay/2")  # 延迟2秒的页面
        
        # 等待特定元素出现
        print("🔍 等待页面元素...")
        await page.wait_for_selector("body")
        
        # 等待网络空闲
        print("🌐 等待网络空闲...")
        await page.wait_for_load_state("networkidle")
        
        # 等待特定条件
        print("⏰ 等待特定条件...")
        await page.wait_for_function("document.readyState === 'complete'")
        
        # 自定义等待
        await page.wait_for_timeout(1000)  # 等待1秒
        
        print("✅ 所有等待策略演示完成!")
        
        await browser.close()

async def main():
    """主函数"""
    import os
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    await network_interception_demo()
    await mobile_simulation_demo()
    await multi_page_demo()
    await javascript_execution_demo()
    await wait_strategies_demo()

if __name__ == "__main__":
    asyncio.run(main())

