#!/usr/bin/env python3
"""
Playwright 批量测试脚本

该脚本用于批量测试多个政务服务网站页面的下载链接功能。
从 Excel 文件中读取测试数据，并将执行结果和时间写回到新的 Excel 文件中。

数据格式要求：
- Excel 文件(.xlsx)
- 必需字段：url, 材料名称, 元素名称
- 输出字段：执行时间, 执行结果

使用方法：
    python batch_runner.py input_file.xlsx
"""
import asyncio
import os
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect
import argparse

class BatchTestRunner:
    """批量测试运行器"""
    
    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = input_file
        self.output_file = output_file or self._generate_output_filename()
        self.download_dir = "downloads"
        self.screenshots_dir = "screenshots"
        self._ensure_directories()
        
    def _generate_output_filename(self) -> str:
        """生成带时间戳的输出文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_path = Path(self.input_file)
        return f"test_results_{timestamp}_{input_path.stem}.xlsx"
        
    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    async def test_single_download_link(self, page, url: str, material_name: str, element_name: str) -> tuple:
        """
        测试单个下载链接
        
        Args:
            page: Playwright页面对象
            url: 目标页面URL
            material_name: 材料名称（用于定位行）
            element_name: 元素名称（下载链接文本）
            
        Returns:
            tuple: (status, message, details, file_type)
                status: "成功" | "失败"  
                message: 详细描述信息
                details: 额外的详细信息（如文件路径等）
                file_type: 文件类型（如"pdf", "doc", "docx"等，失败时为空字符串）
        """
        start_time = datetime.now()
        
        try:
            # --- 1. 页面导航 ---
            print(f"🚀 正在访问: {url}")
            response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            if not response or not response.ok:
                return ("失败", f"页面访问失败，状态码: {response.status if response else '无响应'}", "", "")
            
            # 等待网络空闲，确保页面内容稳定
            print("⏳ 等待页面完全加载稳定...")
            try:
                await page.wait_for_load_state("networkidle", timeout=15000)
                print("✅ 页面已稳定")
            except Exception as e:
                print(f"⚠️ 等待页面稳定超时: {e}")
                # 即使超时也继续执行，因为有些页面可能一直有后台请求
                
            # --- 2. 定位目标行 ---
            print(f"🔍 正在定位材料: {material_name}")
            
            # 改进的定位策略：直接查找包含下载链接的行
            target_row = None
            found = False
            
            # 方案1：查找同时包含材料名称和下载链接的行
            try:
                potential_rows = page.locator(f"tr:has-text('{material_name}')")
                row_count = await potential_rows.count()
                print(f"📋 找到 {row_count} 个包含'{material_name}'的行")
                
                # 遍历每一行，找到包含下载链接的那一行
                for i in range(row_count):
                    row = potential_rows.nth(i)
                    # 检查这一行是否包含目标下载链接
                    link_count = await row.locator(f"a:text('{element_name}')").count()
                    
                    if link_count > 0:
                        # 进一步验证这是正确的行（检查链接是否可点击）
                        links = row.locator(f"a:text('{element_name}')")
                        
                        # 检查链接的属性，确保它们是下载链接
                        first_link = links.first
                        href = await first_link.get_attribute("href")
                        onclick = await first_link.get_attribute("onclick")
                        class_name = await first_link.get_attribute("class")
                        
                        # 如果有href、onclick或特定class，说明是有效的下载链接
                        if href or onclick or (class_name and ("kbbg" in class_name or "download" in class_name.lower())):
                            target_row = row
                            found = True
                            print(f"✅ 找到有效的下载链接行 (第 {i+1} 行)")
                            break
                        else:
                            print(f"⏭️  跳过第 {i+1} 行 (无有效下载链接)")
                
                if not found:
                    # 备用方案：如果上面的严格检查没找到，选择第一个包含链接的行
                    print("🔄 使用备用方案：选择第一个包含链接文本的行")
                    for i in range(row_count):
                        row = potential_rows.nth(i)
                        link_count = await row.locator(f"a:text('{element_name}')").count()
                        if link_count > 0:
                            target_row = row
                            found = True
                            print(f"⚠️  选择第 {i+1} 行作为目标行")
                            break
                            
            except Exception as e:
                print(f"⚠️  定位过程中出现异常: {e}")
            
            if not found or target_row is None:
                return ("失败", f"未找到包含'{material_name}'和'{element_name}'的有效行", "", "")
            
            # 等待行可见
            try:
                await expect(target_row).to_be_visible(timeout=10000)
                print("✅ 目标行已确认可见")
            except Exception as e:
                return ("失败", f"目标行不可见: {e}", "", "")
            
            # --- 3. 定位下载链接 ---
            print(f"🔗 正在定位下载链接: {element_name}")
            
            # 查找目标链接
            target_links = target_row.locator(f"a:text('{element_name}')")
            link_count = await target_links.count()
            
            if link_count == 0:
                return ("失败", f"在目标行中未找到'{element_name}'链接", "", "")
            
            # 选择合适的链接
            if link_count > 1:
                # 优先选择特定class的链接
                preferred_link = target_row.locator(f"a.kbbg:text('{element_name}')")
                if await preferred_link.count() > 0:
                    download_link = preferred_link
                else:
                    download_link = target_links.first
            else:
                download_link = target_links
                
            # 确认链接可见
            await expect(download_link).to_be_visible(timeout=5000)
            
            # --- 4. 执行下载 ---
            print(f"📥 准备下载: {element_name}")
            
            # 检查链接属性
            href = await download_link.get_attribute("href")
            onclick = await download_link.get_attribute("onclick")
            target = await download_link.get_attribute("target")
            
            print(f"🔍 链接信息: href={href is not None}, onclick={onclick is not None}, target={target}")
            
            try:
                # 只有一种策略：必须成功触发下载
                print("🎯 尝试监听并触发下载...")
                
                # 如果链接在新窗口打开，需要处理新页面
                if target == "_blank":
                    print("🔗 检测到新窗口链接，将在新窗口中处理下载")
                    async with page.context.expect_page() as new_page_info:
                        await download_link.click()
                    
                    new_page = await new_page_info.value
                    
                    # 等待新页面稳定
                    print("⏳ 等待新窗口页面稳定...")
                    try:
                        await new_page.wait_for_load_state("networkidle", timeout=10000)
                        print("✅ 新窗口页面已稳定")
                    except Exception as e:
                        print(f"⚠️ 新窗口页面稳定等待超时: {e}")
                    
                    # 在新页面中等待下载事件
                    async with new_page.expect_download(timeout=10000) as download_info:
                        # 有些页面在新窗口打开后会自动触发下载，无需再次点击
                        # 如果需要进一步操作才能下载，需要在这里添加
                        print("⏳ 等待新窗口中的下载...")
                        
                    download = await download_info.value
                    
                    # 下载完成后关闭新页面
                    await new_page.close()
                    
                else:
                    # 在当前页面处理下载
                    async with page.expect_download(timeout=10000) as download_info:
                        await download_link.click()
                    
                    download = await download_info.value
                
                # --- 下载成功处理 ---
                # 构建文件保存路径
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{download.suggested_filename}"
                file_path = os.path.join(self.download_dir, filename)
                
                # 保存文件
                await download.save_as(file_path)
                
                # --- 判断文件类型 ---
                # 从文件名提取扩展名并转换为小写
                _, file_extension = os.path.splitext(download.suggested_filename)
                file_type = file_extension.lower().lstrip('.') if file_extension else ""
                
                elapsed = datetime.now() - start_time
                return ("成功", f"下载完成，耗时: {elapsed.total_seconds():.2f}秒", file_path, file_type)
                
            except Exception as e:
                # 捕获所有下载相关的错误（包括超时）
                print(f"❌ 下载失败: {e}")
                elapsed = datetime.now() - start_time
                return ("失败", f"链接可点击，但未在10秒内触发下载。错误: {str(e)[:100]}... 耗时: {elapsed.total_seconds():.2f}秒", "", "")
            
        except Exception as e:
            elapsed = datetime.now() - start_time
            error_msg = f"执行出错: {str(e)}, 耗时: {elapsed.total_seconds():.2f}秒"
            
            # 保存错误截图
            try:
                screenshot_name = f"error_{material_name}_{element_name}_{datetime.now().strftime('%H%M%S')}.png"
                await page.screenshot(path=f"{self.screenshots_dir}/{screenshot_name}", full_page=True)
                error_msg += f", 截图: {screenshot_name}"
            except:
                pass
                
            return ("失败", error_msg, "", "")
    
    async def run_batch_tests(self):
        """执行批量测试"""
        
        # --- 1. 读取输入数据 ---
        print(f"📖 正在读取输入文件: {self.input_file}")
        
        try:
            df = pd.read_excel(self.input_file)
            print(f"✅ 成功读取 {len(df)} 行数据")
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return
            
        # 检查必需的列
        required_columns = ['url', '材料名称', '元素名称']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ 缺少必需的列: {missing_columns}")
            return
            
        # 添加结果列
        df['执行时间'] = ""
        df['执行结果'] = ""
        df['文件格式'] = ""
        
        # --- 2. 初始化浏览器 ---
        print("\n🌐 正在初始化浏览器...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(accept_downloads=True)
            
            # --- 3. 批量执行测试 ---
            total_count = len(df)
            success_count = 0
            
            for index, row in df.iterrows():
                current_num = index + 1
                url = row['url']
                material_name = row['材料名称'] 
                element_name = row['元素名称']
                
                print(f"\n{'='*60}")
                print(f"📋 执行测试 [{current_num}/{total_count}]")
                print(f"   URL: {url}")
                print(f"   材料: {material_name}")
                print(f"   元素: {element_name}")

                # if material_name != "往来港澳通行证":
                #     continue

                # 创建新页面
                page = await context.new_page()
                
                try:
                    # 执行单个测试
                    status, message, details, file_type = await self.test_single_download_link(
                        page, url, material_name, element_name
                    )
                    
                    # 记录结果
                    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df.at[index, '执行时间'] = execution_time
                    df.at[index, '执行结果'] = f"{status}: {message}"
                    df.at[index, '文件格式'] = file_type if file_type else ""
                    
                    if status == "成功":
                        success_count += 1
                        print(f"✅ {message}")
                        if details:
                            print(f"   文件: {details}")
                        if file_type:
                            print(f"   格式: {file_type}")
                    else:
                        print(f"❌ {message}")
                        
                except Exception as e:
                    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df.at[index, '执行时间'] = execution_time
                    df.at[index, '执行结果'] = f"失败: 未预期的错误 - {e}"
                    df.at[index, '文件格式'] = ""  # 发生异常时文件格式为空
                    print(f"❌ 未预期的错误: {e}")
                
                finally:
                    await page.close()
                    
            # --- 4. 保存结果 ---
            print(f"\n{'='*60}")
            print(f"📊 测试完成!")
            print(f"   总计: {total_count} 条")
            print(f"   成功: {success_count} 条")
            print(f"   失败: {total_count - success_count} 条")
            print(f"   成功率: {(success_count/total_count)*100:.1f}%")
            
            await browser.close()
            
        # --- 5. 输出结果文件 ---
        print(f"\n💾 正在保存结果到: {self.output_file}")
        try:
            df.to_excel(self.output_file, index=False)
            print(f"✅ 结果文件保存成功!")
            
            # 显示结果摘要
            print(f"\n📋 结果摘要:")
            success_rows = df[df['执行结果'].str.contains('成功', na=False)]
            failure_rows = df[df['执行结果'].str.contains('失败', na=False)]
            
            print(f"   ✅ 成功: {len(success_rows)} 条")
            print(f"   ❌ 失败: {len(failure_rows)} 条")
            
            if len(failure_rows) > 0:
                print(f"\n🔍 失败详情:")
                for _, row in failure_rows.iterrows():
                    print(f"   - {row['材料名称']} / {row['元素名称']}: {row['执行结果']}")
                    
        except Exception as e:
            print(f"❌ 保存结果文件失败: {e}")

async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量测试下载链接功能')
    parser.add_argument('input_file', nargs='?', default='sample_test_data.xlsx', help='输入的Excel文件路径（默认: sample_test_data.xlsx）')
    parser.add_argument('-o', '--output', help='输出的Excel文件路径（可选）')
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"❌ 输入文件不存在: {args.input_file}")
        return
        
    # 创建并运行批量测试
    runner = BatchTestRunner(args.input_file, args.output)
    await runner.run_batch_tests()

if __name__ == "__main__":
    asyncio.run(main())
