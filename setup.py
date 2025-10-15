#!/usr/bin/env python3
"""
Playwright Demo 项目安装脚本
运行此脚本来安装依赖和浏览器
"""
import subprocess
import sys

def run_command(command):
    """运行命令并打印输出"""
    print(f"执行命令: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def main():
    print("🚀 开始安装 Playwright Demo 项目...")
    
    # 安装 Python 依赖
    print("\n📦 安装 Python 依赖...")
    if not run_command("pip install -r requirements.txt"):
        print("❌ 安装 Python 依赖失败")
        sys.exit(1)
    
    # 安装浏览器
    print("\n🌐 安装浏览器...")
    if not run_command("playwright install"):
        print("❌ 安装浏览器失败")
        sys.exit(1)
    
    print("\n✅ 安装完成！")
    print("\n🎉 现在您可以运行演示脚本了:")
    print("  python examples/basic_example.py")
    print("  python examples/advanced_example.py")
    print("  pytest tests/")

if __name__ == "__main__":
    main()
