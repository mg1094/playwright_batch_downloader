#!/usr/bin/env python3
"""
Playwright 下载功能演示

该脚本演示了如何自动化以下流程：
1. 访问指定的政务服务网站页面。
2. 检查页面是否可访问。
3. 定位到包含特定文本（“体检合格证明”）的表格行。
4. 在该行内找到“空白表格”和“示例样表”的下载链接。
5. 监听下载事件，并点击链接以下载文件。
6. 将下载的文件保存到本地。
"""
import asyncio
import os
from playwright.async_api import async_playwright, expect

async def main():
    """主执行函数"""
    
    # 定义下载文件保存的目录
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    print(f"📁 文件将下载到: {os.path.abspath(download_dir)}")
    
    async with async_playwright() as p:
        # 启动浏览器，headless=False 可以显示浏览器界面，便于调试
        browser = await p.chromium.launch(headless=False)
        
        # 创建一个新的浏览器上下文，并启用接受下载
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        
        # 目标页面的URL
        url = "https://sz.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=113205000141492526332010502800201&ql_kind=01&iddept_ql_inf=1132050001414925263320105028002"
        
        # --- 1. 检查页面可访问性 ---
        print(f"\n🚀 正在导航到页面: {url}")
        try:
            # 使用 goto 方法访问页面，并设置较长的超时时间
            response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 检查HTTP响应状态
            if response and response.ok:
                print(f"✅ 页面加载成功! 状态码: {response.status}")
            else:
                print(f"❌ 页面加载失败! 状态码: {response.status if response else '无响应'}")
                await browser.close()
                return
        except Exception as e:
            print(f"❌ 导航到页面时发生错误: {e}")
            await browser.close()
            return
            
        # --- 2. 定位目标元素 ---
        print("\n🔍 正在定位'体检合格证明'所在的行...")
        try:
            # 使用更精确的定位策略：定位到同时包含"体检合格证明"和"空白表格"的行
            # 这样可以避免误选到表头行
            target_row = page.locator("tr:has-text('体检合格证明'):has-text('空白表格')")
            
            # 如果上述定位器仍然找不到，尝试备用方案
            row_count = await target_row.count()
            if row_count == 0:
                print("🔄 尝试备用定位方案...")
                # 方案2：通过class属性定位（从错误信息看到有tsize类）
                target_row = page.locator("tr.tsize:has-text('体检合格证明')")
                row_count = await target_row.count()
                
            if row_count == 0:
                print("🔄 尝试第三种定位方案...")
                # 方案3：先找到所有包含"体检合格证明"的行，然后选择包含链接的那一行
                all_rows = page.locator("tr:has-text('体检合格证明')")
                for i in range(await all_rows.count()):
                    row = all_rows.nth(i)
                    # 检查这一行是否包含"空白表格"链接
                    link_count = await row.locator("a:has-text('空白表格')").count()
                    if link_count > 0:
                        target_row = row
                        break
                        
            # 使用expect断言，等待该行元素在10秒内变为可见状态
            await expect(target_row).to_be_visible(timeout=10000)
            # await page.screenshot(path="screenshots/location_success.png", full_page=True)
            print("✅ 成功定位到目标行。")
        except Exception as e:
            print(f"❌ 定位目标行失败: {e}")
            
            # 保存调试信息
            print("🔧 正在收集调试信息...")
            try:
                # 查找所有包含"体检合格证明"的行
                all_health_rows = page.locator("tr:has-text('体检合格证明')")
                health_count = await all_health_rows.count()
                print(f"📊 找到 {health_count} 个包含'体检合格证明'的行")
                
                for i in range(health_count):
                    row = all_health_rows.nth(i)
                    row_text = await row.text_content()
                    print(f"   行 {i+1}: {row_text[:100]}...")
                    
            except Exception as debug_e:
                print(f"⚠️  调试信息收集失败: {debug_e}")
                
            await page.screenshot(path="screenshots/error_location_failed.png", full_page=True)
            print("📸 已保存错误截图: screenshots/error_location_failed.png")
            await browser.close()
            return
            
        # 在已定位的行内查找下载链接
        print("🔍 正在行内查找'空白表格'和'示例样表'链接...")
        
        # 检查有多少个"空白表格"链接
        blank_form_links = target_row.locator("a:text('空白表格')")
        blank_form_count = await blank_form_links.count()
        print(f"📋 找到 {blank_form_count} 个'空白表格'链接")
        
        # 检查有多少个"示例样表"链接  
        sample_form_links = target_row.locator("a:text('示例样表')")
        sample_form_count = await sample_form_links.count()
        print(f"📄 找到 {sample_form_count} 个'示例样表'链接")
        
        # 如果有多个链接，选择第一个或者根据class属性选择
        if blank_form_count > 1:
            print("🔧 发现多个'空白表格'链接，尝试选择合适的链接...")
            # 优先选择class为"kbbg"的链接（通常是主要链接）
            blank_form_link = target_row.locator("a.kbbg:text('空白表格')")
            if await blank_form_link.count() == 0:
                # 如果没找到，就选择第一个
                blank_form_link = blank_form_links.first
        else:
            blank_form_link = blank_form_links
            
        if sample_form_count > 1:
            print("🔧 发现多个'示例样表'链接，尝试选择合适的链接...")
            # 优先选择class为"kbbg"的链接
            sample_form_link = target_row.locator("a.kbbg:text('示例样表')")
            if await sample_form_link.count() == 0:
                # 如果没找到，就选择第一个
                sample_form_link = sample_form_links.first
        else:
            sample_form_link = sample_form_links
        
        # 确认链接可见
        try:
            await expect(blank_form_link).to_be_visible(timeout=5000)
            await expect(sample_form_link).to_be_visible(timeout=5000)
            print("✅ 成功定位到下载链接。")
        except Exception as e:
            print(f"⚠️  链接可见性检查失败: {e}")
            # 打印链接详细信息帮助调试
            try:
                for i in range(blank_form_count):
                    link = blank_form_links.nth(i)
                    class_name = await link.get_attribute("class")
                    href = await link.get_attribute("href")
                    onclick = await link.get_attribute("onclick")
                    print(f"   空白表格链接 {i+1}: class='{class_name}', href='{href}', onclick存在={onclick is not None}")
                
                for i in range(sample_form_count):
                    link = sample_form_links.nth(i)
                    class_name = await link.get_attribute("class")
                    href = await link.get_attribute("href")
                    onclick = await link.get_attribute("onclick")
                    print(f"   示例样表链接 {i+1}: class='{class_name}', href='{href}', onclick存在={onclick is not None}")
            except Exception:
                pass
            raise
        
        # --- 3. 执行并验证下载 ---
        
        # 下载 "空白表格"
        print("\n📥 准备下载'空白表格'...")
        try:
            # page.expect_download() 会创建一个监听器，等待下载事件发生
            async with page.expect_download() as download_info:
                # 点击链接以触发下载
                await blank_form_link.click()
            
            download = await download_info.value
            
            # 构建保存路径
            file_path_blank = os.path.join(download_dir, download.suggested_filename)
            
            # 保存文件
            await download.save_as(file_path_blank)
            print(f"✅ '空白表格'下载成功! 文件保存在: {file_path_blank}")
            
        except Exception as e:
            print(f"❌ 下载'空白表格'时发生错误: {e}")

        # 下载 "示例样表"
        print("\n📥 准备下载'示例样表'...")
        try:
            async with page.expect_download() as download_info:
                await sample_form_link.click()
            
            download = await download_info.value
            file_path_sample = os.path.join(download_dir, download.suggested_filename)
            await download.save_as(file_path_sample)
            print(f"✅ '示例样表'下载成功! 文件保存在: {file_path_sample}")
            
        except Exception as e:
            print(f"❌ 下载'示例样表'时发生错误: {e}")

        # --- 4. 清理 ---
        print("\n🎉 任务完成，关闭浏览器。")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
