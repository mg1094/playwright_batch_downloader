"""
Playwright 工具函数
提供常用的辅助功能
"""
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from playwright.async_api import Page, Browser, BrowserContext

class PlaywrightHelper:
    """Playwright 辅助工具类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.screenshots_dir = "screenshots"
        self.logs_dir = "logs"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保目录存在"""
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    async def safe_goto(self, url: str, timeout: int = 30000) -> bool:
        """安全地访问页面"""
        try:
            await self.page.goto(url, timeout=timeout)
            await self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print(f"访问页面失败: {url}, 错误: {e}")
            return False
    
    async def safe_click(self, selector: str, timeout: int = 10000) -> bool:
        """安全地点击元素"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            return True
        except Exception as e:
            print(f"点击元素失败: {selector}, 错误: {e}")
            return False
    
    async def safe_fill(self, selector: str, text: str, timeout: int = 10000) -> bool:
        """安全地填写表单"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, text)
            return True
        except Exception as e:
            print(f"填写表单失败: {selector}, 错误: {e}")
            return False
    
    async def wait_for_element(self, selector: str, timeout: int = 10000) -> bool:
        """等待元素出现"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception:
            return False
    
    async def get_element_text(self, selector: str) -> Optional[str]:
        """获取元素文本"""
        try:
            element = self.page.locator(selector)
            return await element.text_content()
        except Exception:
            return None
    
    async def get_element_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """获取元素属性"""
        try:
            element = self.page.locator(selector)
            return await element.get_attribute(attribute)
        except Exception:
            return None
    
    async def is_element_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        try:
            element = self.page.locator(selector)
            return await element.is_visible()
        except Exception:
            return False
    
    async def take_screenshot(self, name: str = None, full_page: bool = True) -> str:
        """截图"""
        if name is None:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        filepath = os.path.join(self.screenshots_dir, name)
        await self.page.screenshot(path=filepath, full_page=full_page)
        return filepath
    
    async def take_element_screenshot(self, selector: str, name: str = None) -> Optional[str]:
        """元素截图"""
        try:
            if name is None:
                name = f"element_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            filepath = os.path.join(self.screenshots_dir, name)
            element = self.page.locator(selector)
            await element.screenshot(path=filepath)
            return filepath
        except Exception as e:
            print(f"元素截图失败: {selector}, 错误: {e}")
            return None
    
    async def get_page_info(self) -> Dict[str, Any]:
        """获取页面信息"""
        return await self.page.evaluate("""
            () => {
                return {
                    title: document.title,
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    elementsCount: {
                        links: document.querySelectorAll('a').length,
                        images: document.querySelectorAll('img').length,
                        forms: document.querySelectorAll('form').length,
                        inputs: document.querySelectorAll('input').length
                    },
                    loadTime: performance.now()
                };
            }
        """)
    
    async def scroll_to_element(self, selector: str) -> bool:
        """滚动到元素"""
        try:
            element = self.page.locator(selector)
            await element.scroll_into_view_if_needed()
            return True
        except Exception:
            return False
    
    async def scroll_page(self, direction: str = "down", pixels: int = 500) -> bool:
        """滚动页面"""
        try:
            if direction.lower() == "down":
                await self.page.evaluate(f"window.scrollBy(0, {pixels})")
            elif direction.lower() == "up":
                await self.page.evaluate(f"window.scrollBy(0, -{pixels})")
            elif direction.lower() == "top":
                await self.page.evaluate("window.scrollTo(0, 0)")
            elif direction.lower() == "bottom":
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            return True
        except Exception:
            return False
    
    async def save_page_source(self, filename: str = None) -> str:
        """保存页面源码"""
        if filename is None:
            filename = f"page_source_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.logs_dir, filename)
        content = await self.page.content()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    async def save_console_logs(self, filename: str = None) -> str:
        """保存控制台日志"""
        if filename is None:
            filename = f"console_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.logs_dir, filename)
        
        # 注意: 这需要在页面加载前设置监听器
        # 在实际使用中，应该在创建Helper时就设置
        logs = []
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        return filepath

class NetworkHelper:
    """网络相关辅助工具"""
    
    def __init__(self, page: Page):
        self.page = page
        self.requests = []
        self.responses = []
        self._setup_listeners()
    
    def _setup_listeners(self):
        """设置网络监听器"""
        self.page.on("request", self._handle_request)
        self.page.on("response", self._handle_response)
    
    def _handle_request(self, request):
        """处理请求"""
        self.requests.append({
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "timestamp": datetime.now().isoformat()
        })
    
    def _handle_response(self, response):
        """处理响应"""
        self.responses.append({
            "url": response.url,
            "status": response.status,
            "headers": dict(response.headers),
            "timestamp": datetime.now().isoformat()
        })
    
    def get_requests_by_domain(self, domain: str) -> List[Dict]:
        """根据域名筛选请求"""
        return [req for req in self.requests if domain in req["url"]]
    
    def get_requests_by_method(self, method: str) -> List[Dict]:
        """根据方法筛选请求"""
        return [req for req in self.requests if req["method"].upper() == method.upper()]
    
    def save_network_logs(self, filename: str = None) -> str:
        """保存网络日志"""
        if filename is None:
            filename = f"network_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        filepath = os.path.join(logs_dir, filename)
        
        data = {
            "requests": self.requests,
            "responses": self.responses,
            "summary": {
                "total_requests": len(self.requests),
                "total_responses": len(self.responses),
                "unique_domains": len(set(req["url"].split("/")[2] for req in self.requests if len(req["url"].split("/")) > 2))
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath

async def create_browser_with_options(browser_type: str = "chromium", headless: bool = True, **kwargs) -> Browser:
    """创建带选项的浏览器"""
    from playwright.async_api import async_playwright
    
    p = await async_playwright().start()
    
    if browser_type.lower() == "chromium":
        browser = await p.chromium.launch(headless=headless, **kwargs)
    elif browser_type.lower() == "firefox":
        browser = await p.firefox.launch(headless=headless, **kwargs)
    elif browser_type.lower() == "webkit":
        browser = await p.webkit.launch(headless=headless, **kwargs)
    else:
        raise ValueError(f"不支持的浏览器类型: {browser_type}")
    
    return browser

async def create_mobile_context(browser: Browser, device_name: str = "iPhone 12") -> BrowserContext:
    """创建移动设备上下文"""
    from playwright.async_api import async_playwright
    
    p = await async_playwright().start()
    device = p.devices.get(device_name)
    
    if not device:
        raise ValueError(f"不支持的设备: {device_name}")
    
    return await browser.new_context(**device)


