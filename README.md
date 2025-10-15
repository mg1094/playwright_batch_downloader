# Playwright Python 演示项目

这是一个完整的 Playwright Python 演示项目，旨在帮助您学习和掌握 Playwright 的各种功能和用法。

## 📋 项目概述

本项目包含了从基础到高级的 Playwright 使用示例，涵盖：
- 基础浏览器操作和页面交互
- 高级功能如网络拦截、移动设备模拟
- 完整的测试用例示例
- 实用的辅助工具函数

## 🗂️ 项目结构

```
playwright_demo/
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖包
├── setup.py              # 自动安装脚本
├── examples/             # 示例脚本目录
│   ├── basic_example.py      # 基础功能演示
│   ├── advanced_example.py   # 高级功能演示
│   └── helper_demo.py        # 辅助工具演示
├── tests/                # 测试用例目录
│   ├── conftest.py           # pytest 配置
│   ├── test_basic_operations.py     # 基础操作测试
│   └── test_advanced_features.py    # 高级功能测试
├── utils/                # 工具函数目录
│   └── helpers.py            # 辅助工具类
├── screenshots/          # 截图保存目录（运行后生成）
└── logs/                # 日志保存目录（运行后生成）
```

## 🚀 快速开始

### 1. 安装依赖

运行自动安装脚本：
```bash
python setup.py
```

或者手动安装：
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装浏览器
playwright install
```

### 2. 运行示例

**基础示例**：
```bash
python examples/basic_example.py
```

**高级功能演示**：
```bash
python examples/advanced_example.py
```

**辅助工具演示**：
```bash
python examples/helper_demo.py
```

**批量下载链接测试**：
```bash
# 首先创建示例测试数据
python examples/create_sample_data.py

# 执行批量测试
python examples/batch_runner.py sample_test_data.xlsx

# 或指定输出文件名
python examples/batch_runner.py sample_test_data.xlsx -o my_results.xlsx
```

### 3. 运行测试

运行所有测试：
```bash
pytest tests/
```

运行特定测试：
```bash
pytest tests/test_basic_operations.py -v
pytest tests/test_advanced_features.py -v
```

## 📚 功能演示

### 基础功能 (basic_example.py)

- ✅ 浏览器启动和页面导航
- ✅ 元素定位和交互
- ✅ 表单填写和提交
- ✅ 页面截图
- ✅ 搜索操作演示

### 高级功能 (advanced_example.py)

- 🔍 **网络拦截**：监控和拦截HTTP请求/响应
- 📱 **移动设备模拟**：模拟不同设备的视口和用户代理
- 🗂️ **多页面管理**：同时管理多个浏览器标签页
- ⚙️ **JavaScript执行**：在页面中执行自定义JavaScript代码
- ⏳ **等待策略**：各种等待条件的使用方法

### 辅助工具 (helper_demo.py)

- 🛠️ **PlaywrightHelper类**：封装常用操作的辅助方法
- 🌐 **NetworkHelper类**：网络请求分析工具
- 📊 **页面信息获取**：自动收集页面统计信息
- 🔒 **安全操作**：带错误处理的操作方法

### 批量测试功能 (batch_runner.py)

- 📊 **Excel数据驱动**：从Excel文件读取测试用例
- 🔄 **批量执行**：自动化执行多个下载链接测试
- 📝 **结果记录**：自动记录执行时间和结果状态
- 💾 **结果输出**：生成带时间戳的结果Excel文件
- 🔍 **详细报告**：提供成功率统计和失败详情
- 📸 **错误截图**：失败时自动保存错误截图

## 🧪 测试用例

### 基础操作测试 (test_basic_operations.py)
- 页面导航测试
- 元素可见性验证
- 文本内容检查
- 表单交互测试
- 等待策略测试

### 高级功能测试 (test_advanced_features.py)
- 网络请求拦截测试
- JavaScript执行测试
- 本地存储操作测试
- Cookie管理测试
- 移动设备模拟测试
- 多页面管理测试

## 🔧 工具类说明

### PlaywrightHelper

提供以下辅助方法：
- `safe_goto()` - 安全的页面导航
- `safe_click()` - 安全的元素点击
- `safe_fill()` - 安全的表单填写
- `take_screenshot()` - 页面截图
- `get_page_info()` - 获取页面信息
- `scroll_to_element()` - 滚动到指定元素

### NetworkHelper

网络相关功能：
- 自动记录所有HTTP请求和响应
- 按域名或方法筛选请求
- 导出网络日志为JSON格式

## 📖 学习路径建议

1. **初学者**：
   - 先运行 `basic_example.py` 了解基础操作
   - 阅读代码注释理解每个步骤
   - 尝试修改示例中的网站URL和操作

2. **进阶学习**：
   - 运行 `advanced_example.py` 学习高级功能
   - 研究网络拦截和移动设备模拟
   - 了解JavaScript执行和多页面管理

3. **实践应用**：
   - 运行 `helper_demo.py` 学习如何封装常用操作
   - 查看测试用例了解最佳实践
   - 尝试编写自己的测试脚本

4. **测试开发**：
   - 学习pytest与Playwright的集成
   - 理解测试夹具(fixtures)的使用
   - 掌握断言和验证方法

## 🎯 实际应用场景

- **Web应用测试**：自动化功能测试、回归测试
- **爬虫开发**：动态网页数据抓取
- **性能监控**：页面加载时间、网络请求分析
- **UI测试**：跨浏览器兼容性测试
- **移动端测试**：响应式设计验证
- **批量链接检测**：政务网站下载链接可用性批量验证

## 📋 批量测试使用指南

### 数据文件格式要求

Excel文件(.xlsx)必须包含以下列：
- **url**: 目标页面的完整URL
- **材料名称**: 用于定位表格行的材料名称文本
- **元素名称**: 下载链接的文本（如"空白表格"、"示例样表"）

其他列可选，执行后会自动添加：
- **执行时间**: 测试执行的时间戳
- **执行结果**: 成功/失败状态及详细信息

### 批量测试步骤

1. **准备测试数据**：
   ```bash
   # 创建示例数据文件
   python examples/create_sample_data.py
   ```

2. **执行批量测试**：
   ```bash
   # 使用默认输出文件名
   python examples/batch_runner.py sample_test_data.xlsx
   
   # 自定义输出文件名
   python examples/batch_runner.py your_data.xlsx -o results_20251015.xlsx
   ```

3. **查看结果**：
   - 测试完成后会生成结果Excel文件
   - 下载的文件保存在 `downloads/` 目录
   - 错误截图保存在 `screenshots/` 目录

### 结果解读

- **成功**: 链接可点击且文件成功下载
- **失败**: 包含具体的错误原因（页面访问失败、元素未找到、下载失败等）
- **执行时间**: 每个测试用例的执行耗时
- **成功率统计**: 整体测试结果概览

## 🔍 常见问题

**Q: 浏览器启动失败？**
A: 确保已运行 `playwright install` 安装浏览器

**Q: 元素定位失败？**
A: 使用 `page.wait_for_selector()` 等待元素加载

**Q: 测试运行缓慢？**
A: 可以设置 `headless=True` 使用无头模式

**Q: 如何调试脚本？**
A: 使用 `page.pause()` 暂停执行，或设置 `slow_mo` 参数

## 📝 更多资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [Playwright Python API 参考](https://playwright.dev/python/docs/api/class-playwright)
- [pytest-playwright 插件](https://github.com/microsoft/playwright-pytest)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个演示项目！

## 📄 许可证

本项目采用 MIT 许可证。


