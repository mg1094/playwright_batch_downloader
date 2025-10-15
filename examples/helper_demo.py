#!/usr/bin/env python3
"""
辅助工具演示
展示如何使用自定义的辅助函数来简化Playwright操作
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright
from utils.helpers import PlaywrightHelper, NetworkHelper

async def helper_demo():
    """辅助工具演示"""
    print("🛠️  辅助工具演示开始...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 创建辅助工具实例
        helper = PlaywrightHelper(page)
        network_helper = NetworkHelper(page)
        
        print("🌐 使用安全导航访问页面...")
        success = await helper.safe_goto("https://httpbin.org/")
        if success:
            print("✅ 页面访问成功")
        else:
            print("❌ 页面访问失败")
            return
        
        # 获取页面信息
        print("📊 获取页面信息...")
        page_info = await helper.get_page_info()
        print(f"页面标题: {page_info['title']}")
        print(f"页面URL: {page_info['url']}")
        print(f"视口大小: {page_info['viewport']['width']} x {page_info['viewport']['height']}")
        print(f"链接数量: {page_info['elementsCount']['links']}")
        
        # 截图
        print("📸 保存页面截图...")
        screenshot_path = await helper.take_screenshot("helper_demo_page.png")
        print(f"截图已保存: {screenshot_path}")
        
        # 测试表单页面
        print("\n📝 访问表单页面...")
        await helper.safe_goto("https://httpbin.org/forms/post")
        
        # 使用安全填写方法
        print("✍️  填写表单...")
        await helper.safe_fill("input[name='custname']", "Playwright Helper 测试")
        await helper.safe_fill("input[name='custtel']", "13800138000")
        await helper.safe_fill("input[name='custemail']", "helper@example.com")
        
        # 检查元素可见性
        submit_button_visible = await helper.is_element_visible("input[type='submit']")
        print(f"提交按钮可见: {submit_button_visible}")
        
        # 获取元素文本
        button_text = await helper.get_element_text("input[type='submit']")
        print(f"按钮文本: {button_text}")
        
        # 表单截图
        form_screenshot = await helper.take_screenshot("helper_demo_form.png")
        print(f"表单截图已保存: {form_screenshot}")
        
        # 滚动测试
        print("\n📜 测试滚动功能...")
        await helper.scroll_page("bottom")
        await asyncio.sleep(1)
        await helper.scroll_page("top")
        
        # 保存页面源码
        print("💾 保存页面源码...")
        source_path = await helper.save_page_source("helper_demo_source.html")
        print(f"页面源码已保存: {source_path}")
        
        # 网络请求分析
        print("\n🔍 分析网络请求...")
        httpbin_requests = network_helper.get_requests_by_domain("httpbin.org")
        get_requests = network_helper.get_requests_by_method("GET")
        
        print(f"httpbin.org 相关请求: {len(httpbin_requests)} 个")
        print(f"GET 请求: {len(get_requests)} 个")
        
        # 保存网络日志
        network_log_path = network_helper.save_network_logs("helper_demo_network.json")
        print(f"网络日志已保存: {network_log_path}")
        
        await browser.close()
        print("✅ 辅助工具演示完成!")

async def mobile_helper_demo():
    """移动设备辅助演示"""
    print("\n📱 移动设备辅助演示...")
    
    from utils.helpers import create_browser_with_options, create_mobile_context
    
    # 创建浏览器
    browser = await create_browser_with_options("chromium", headless=False)
    
    # 创建移动设备上下文
    mobile_context = await create_mobile_context(browser, "iPhone 12")
    page = await mobile_context.new_page()
    
    # 创建辅助工具
    helper = PlaywrightHelper(page)
    
    print("📱 使用移动设备访问页面...")
    await helper.safe_goto("https://httpbin.org/")
    
    # 获取移动设备信息
    page_info = await helper.get_page_info()
    print(f"移动设备视口: {page_info['viewport']['width']} x {page_info['viewport']['height']}")
    print(f"用户代理: {page_info['userAgent'][:50]}...")
    
    # 移动设备截图
    mobile_screenshot = await helper.take_screenshot("helper_mobile_demo.png")
    print(f"移动设备截图已保存: {mobile_screenshot}")
    
    await browser.close()
    print("✅ 移动设备辅助演示完成!")

async def main():
    """主函数"""
    await helper_demo()
    await mobile_helper_demo()

if __name__ == "__main__":
    asyncio.run(main())


