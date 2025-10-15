"""
基础操作测试用例
测试页面导航、元素交互等基本功能
"""
import pytest
from playwright.async_api import Page, expect

class TestBasicOperations:
    """基础操作测试类"""
    
    @pytest.mark.asyncio
    async def test_page_navigation(self, page: Page):
        """测试页面导航"""
        # 访问测试页面
        await page.goto("https://httpbin.org/")
        
        # 验证页面标题
        await expect(page).to_have_title("httpbin.org")
        
        # 验证URL
        expect(page.url).to_contain("httpbin.org")
    
    @pytest.mark.asyncio
    async def test_element_visibility(self, page: Page):
        """测试元素可见性"""
        await page.goto("https://httpbin.org/")
        
        # 检查主标题是否可见
        main_heading = page.locator("h1")
        await expect(main_heading).to_be_visible()
        
        # 检查导航链接
        links = page.locator("a")
        await expect(links.first).to_be_visible()
    
    @pytest.mark.asyncio
    async def test_text_content(self, page: Page):
        """测试文本内容"""
        await page.goto("https://httpbin.org/")
        
        # 获取并验证页面标题文本
        heading = page.locator("h1")
        await expect(heading).to_contain_text("httpbin")
    
    @pytest.mark.asyncio
    async def test_form_interaction(self, page: Page):
        """测试表单交互"""
        await page.goto("https://httpbin.org/forms/post")
        
        # 填写表单字段
        await page.fill("input[name='custname']", "测试用户")
        await page.fill("input[name='custtel']", "13800138000")
        await page.fill("input[name='custemail']", "test@example.com")
        
        # 验证输入值
        name_input = page.locator("input[name='custname']")
        await expect(name_input).to_have_value("测试用户")
        
        # 选择下拉选项
        await page.select_option("select[name='size']", "large")
        
        # 验证选择
        size_select = page.locator("select[name='size']")
        await expect(size_select).to_have_value("large")
    
    @pytest.mark.asyncio
    async def test_checkbox_and_radio(self, page: Page):
        """测试复选框和单选按钮"""
        await page.goto("https://httpbin.org/forms/post")
        
        # 选择单选按钮
        bacon_radio = page.locator("input[value='bacon']")
        await bacon_radio.check()
        await expect(bacon_radio).to_be_checked()
        
        # 测试另一个单选按钮
        cheese_radio = page.locator("input[value='cheese']")
        await cheese_radio.check()
        await expect(cheese_radio).to_be_checked()
        await expect(bacon_radio).not_to_be_checked()  # 之前的应该被取消
    
    @pytest.mark.asyncio
    async def test_wait_for_element(self, page: Page):
        """测试等待元素"""
        await page.goto("https://httpbin.org/delay/1")
        
        # 等待页面加载完成
        await page.wait_for_load_state("networkidle")
        
        # 等待特定元素出现
        body = page.locator("body")
        await expect(body).to_be_visible()
    
    @pytest.mark.asyncio
    async def test_screenshot(self, page: Page):
        """测试截图功能"""
        await page.goto("https://httpbin.org/")
        
        # 全页面截图
        screenshot = await page.screenshot()
        assert len(screenshot) > 0
        
        # 元素截图
        heading = page.locator("h1")
        element_screenshot = await heading.screenshot()
        assert len(element_screenshot) > 0

