#!/usr/bin/env python3
"""
Playwright 基础示例
演示基本的浏览器操作和页面交互
"""
import asyncio
from playwright.async_api import async_playwright

async def basic_browser_operations():
    """基础浏览器操作演示"""
    print("🌐 启动浏览器...")
    
    async with async_playwright() as p:
        # 启动浏览器（可以选择 chromium, firefox, webkit）
        browser = await p.chromium.launch(headless=False)  # headless=False 显示浏览器窗口
        page = await browser.new_page()
        
        print("📖 访问百度首页...")
        # await page.goto("https://www.baidu.com")
        # await page.goto("https://yqlb.jszwfw.gov.cn:1718/jssyqlb/indexnew.html")
        
        # 使用更稳定的导航方式
        try:
            response = await page.goto(
                "https://sz.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=113205000141492526332010502800201&ql_kind=01&iddept_ql_inf=1132050001414925263320105028002",
                wait_until="domcontentloaded",  # 等待DOM内容加载完成
                timeout=30000  # 30秒超时
            )
            
            if response and response.ok:
                print(f"✅ 页面加载成功，状态码: {response.status}")
            else:
                print(f"⚠️  页面加载可能有问题，状态码: {response.status if response else '无响应'}")
                
        except Exception as e:
            print(f"❌ 页面加载失败: {e}")
            await browser.close()
            return
        
        # 等待页面完全加载并稳定
        try:
            # 等待DOM内容加载
            await page.wait_for_load_state("domcontentloaded", timeout=10000)
            print("✅ DOM内容加载完成")
            
            # 等待网络空闲（可选）
            try:
                await page.wait_for_load_state("networkidle", timeout=5000)
                print("✅ 网络活动已稳定")
            except:
                print("⚠️  网络活动检测超时，继续执行")
                
        except Exception as e:
            print(f"⚠️  等待页面加载时出错: {e}")
        
        # 获取页面标题（增加错误处理）
        try:
            title = await page.title()
            print(f"📄 页面标题: {title}")
        except Exception as e:
            print(f"⚠️  无法获取页面标题: {e}")
            title = "未知标题"
        
        # 截图（增加错误处理）
        try:
            await page.screenshot(path="screenshots/baidu_homepage.png")
            print("📸 已保存截图到 screenshots/baidu_homepage.png")
        except Exception as e:
            print(f"⚠️  截图失败: {e}")
        
        # 检查页面内容是否加载完成
        try:
            # 等待页面主要内容出现
            await page.wait_for_timeout(2000)  # 额外等待2秒确保页面稳定
            
            # 获取一些基本信息
            url = page.url
            print(f"🌐 当前页面URL: {url}")
            
        except Exception as e:
            print(f"⚠️  获取页面信息时出错: {e}")
        
        try:
            # 等待页面内容加载
            await page.wait_for_load_state("domcontentloaded")
            
            # 查找包含"体检合格证明"文本的元素
            health_cert_elements = page.locator("text=体检合格证明")
            health_cert_count = await health_cert_elements.count()
            
            if health_cert_count > 0:
                print(f"✅ 找到 {health_cert_count} 个包含'体检合格证明'的元素")
                
                # 查找附近的链接，可能是"空白表格"和"示例样表"
                # 查找页面中所有的链接
                all_links = page.locator("a")
                link_count = await all_links.count()
                print(f"📊 页面中共有 {link_count} 个链接")
                
                # 检查包含特定文本的链接
                blank_form_links = page.locator("a:text('空白表格')")
                sample_form_links = page.locator("a:text('示例样表')")
                
                blank_form_count = await blank_form_links.count()
                sample_form_count = await sample_form_links.count()
                
                print(f"📋 找到 {blank_form_count} 个'空白表格'链接")
                print(f"📄 找到 {sample_form_count} 个'示例样表'链接")
                
                # 检查每个链接的可点击性和下载属性
                for i in range(blank_form_count):
                    link = blank_form_links.nth(i)
                    
                    # 检查链接是否可见
                    is_visible = await link.is_visible()
                    # 检查链接是否可用
                    is_enabled = await link.is_enabled()
                    # 获取链接文本
                    text = await link.text_content()
                    # 获取链接地址
                    href = await link.get_attribute("href")
                    # 检查是否有download属性
                    download_attr = await link.get_attribute("download")
                    
                    print(f"\n🔗 空白表格链接 {i+1}:")
                    print(f"   文本: {text}")
                    print(f"   是否可见: {is_visible}")
                    print(f"   是否可用: {is_enabled}")
                    print(f"   链接地址: {href}")
                    print(f"   下载属性: {download_attr}")
                    
                    if is_visible and is_enabled:
                        print("   ✅ 此链接可以点击")
                        # 可以尝试点击下载（注释掉，需要时取消注释）
                        # await link.click()
                        # print("   📥 已尝试点击下载")
                    else:
                        print("   ❌ 此链接无法点击")
                
                for i in range(sample_form_count):
                    link = sample_form_links.nth(i)
                    
                    # 检查链接是否可见
                    is_visible = await link.is_visible()
                    # 检查链接是否可用
                    is_enabled = await link.is_enabled()
                    # 获取链接文本
                    text = await link.text_content()
                    # 获取链接地址
                    href = await link.get_attribute("href")
                    # 检查是否有download属性
                    download_attr = await link.get_attribute("download")
                    
                    print(f"\n🔗 示例样表链接 {i+1}:")
                    print(f"   文本: {text}")
                    print(f"   是否可见: {is_visible}")
                    print(f"   是否可用: {is_enabled}")
                    print(f"   链接地址: {href}")
                    print(f"   下载属性: {download_attr}")
                    
                    if is_visible and is_enabled:
                        print("   ✅ 此链接可以点击")
                        # 可以尝试点击下载（注释掉，需要时取消注释）
                        # await link.click()
                        # print("   📥 已尝试点击下载")
                    else:
                        print("   ❌ 此链接无法点击")
                        
            else:
                print("❌ 未找到包含'体检合格证明'的元素")
                # 如果找不到，可以打印页面内容帮助调试
                page_text = await page.text_content("body")
                if "体检合格证明" in page_text:
                    print("⚠️  页面文本中包含'体检合格证明'，但可能结构不同")
                else:
                    print("❌ 页面文本中不包含'体检合格证明'")
                
        except Exception as e:
            print(f"❌ 检查链接时发生错误: {e}")



        
        # 搜索操作
        # print("🔍 执行搜索...")
        # # 这个符号 "#" 是 CSS 选择器中的ID选择器，"#kw" 表示选择id为"kw"的元素（即百度首页的搜索框）
        # search_box = page.locator("#chat-textarea")
        # await search_box.fill("Playwright Python")
        # await search_box.press("Enter")
        
        # # 等待搜索结果加载
        # await page.wait_for_selector(".result")
        
        # # 获取搜索结果
        # results = page.locator(".result h3")
        # count = await results.count()
        # print(f"📊 找到 {count} 个搜索结果")
        
        # # 打印前5个搜索结果标题
        # for i in range(min(5, count)):
        #     result_text = await results.nth(i).text_content()
        #     print(f"  {i+1}. {result_text}")
        
        # # 截图搜索结果
        # await page.screenshot(path="screenshots/search_results.png")
        # print("📸 已保存搜索结果截图")
        
        await browser.close()
        print("✅ 基础示例执行完成!")

async def form_interaction_demo():
    """表单交互演示"""
    print("\n📝 表单交互演示...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 访问一个测试表单网站
        await page.goto("https://httpbin.org/forms/post")
        
        # 填写表单
        await page.fill("input[name='custname']", "张三")
        await page.fill("input[name='custtel']", "13800138000")
        await page.fill("input[name='custemail']", "zhangsan@example.com")
        await page.fill("textarea[name='comments']", "这是一个 Playwright 测试")
        
        # 选择下拉菜单
        await page.select_option("select[name='size']", "medium")
        
        # 选择单选按钮
        await page.check("input[value='bacon']")
        
        print("📝 表单已填写完成")
        await page.screenshot(path="screenshots/form_filled.png")
        
        # 提交表单
        await page.click("input[type='submit']")
        
        # 等待响应页面
        await page.wait_for_load_state("networkidle")
        
        # 获取提交结果
        result_text = await page.text_content("body")
        print("📤 表单提交结果已获取")
        
        await page.screenshot(path="screenshots/form_submitted.png")
        
        await browser.close()
        print("✅ 表单交互演示完成!")

async def main():
    """主函数"""
    # 创建截图目录
    import os
    os.makedirs("screenshots", exist_ok=True)
    
    await basic_browser_operations()
    # await form_interaction_demo()

if __name__ == "__main__":
    asyncio.run(main())
