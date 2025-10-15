#!/usr/bin/env python3
"""
创建示例测试数据文件
生成一个包含测试数据的Excel文件，供批量测试使用
"""
import pandas as pd

def create_sample_data():
    """创建示例测试数据"""
    
    # 根据您图片中的数据创建示例数据
    test_data = [
        {
            "序号": 1,
            "事项类型": "事项巡检",
            "事项名称": "招聘会员位预约",
            "检测类型": "事项巡检",
            "url": "https://www.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=1132050001414925263320105028002",
            "材料名称": "招聘会员位申请",
            "元素名称": "空白表格",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 2,
            "事项类型": "事项巡检",
            "事项名称": "招聘会员位预约",
            "检测类型": "事项巡检", 
            "url": "https://www.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=1132050001414925263320105028002",
            "材料名称": "招聘会员位申请",
            "元素名称": "示例样表",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 3,
            "事项类型": "事项巡检",
            "事项名称": "我省居民赴港澳探亲签注的许可",
            "检测类型": "事项巡检",
            "url": "https://www.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=1132050001414925263320105028002", 
            "材料名称": "证明相应亲属关系文件",
            "元素名称": "示例样表",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 4,
            "事项类型": "事项巡检", 
            "事项名称": "我省居民赴港澳探亲签注的许可",
            "检测类型": "事项巡检",
            "url": "https://www.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=1132050001414925263320105028002",
            "材料名称": "往来港澳通行证",
            "元素名称": "示例样表", 
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 5,
            "事项类型": "事项巡检",
            "事项名称": "我省居民赴港澳探亲签注的许可",
            "检测类型": "事项巡检",
            "url": "https://www.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=1132050001414925263320105028002",
            "材料名称": "中国公民出入境证件申请表",
            "元素名称": "空白表格",
            "元素类型": "下载链接", 
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 6,
            "事项类型": "事项巡检",
            "事项名称": "我省居民赴港澳探亲签注的许可", 
            "检测类型": "事项巡检",
            "url": "https://www.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=1132050001414925263320105028002",
            "材料名称": "中国公民出入境证件申请表",
            "元素名称": "示例样表",
            "元素类型": "下载链接",
            "执行方式": "playwright", 
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 7,
            "事项类型": "事项巡检",
            "事项名称": "江苏省新型冠状病毒肺炎疫情防控", 
            "检测类型": "事项巡检",
            "url": "https://sz.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=113205000141492526332010502800201&ql_kind=01&iddept_ql_inf=1132050001414925263320105028002",
            "材料名称": "江苏省新型冠状病毒检测体检表",
            "元素名称": "空白表格",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 8,
            "事项类型": "事项巡检",
            "事项名称": "江苏省新型冠状病毒肺炎疫情防控",
            "检测类型": "事项巡检", 
            "url": "https://sz.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=113205000141492526332010502800201&ql_kind=01&iddept_ql_inf=1132050001414925263320105028002",
            "材料名称": "江苏省新型冠状病毒检测体检表",
            "元素名称": "示例样表",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 9,
            "事项类型": "事项巡检",
            "事项名称": "江苏省新型冠状病毒肺炎疫情防控",
            "检测类型": "事项巡检",
            "url": "https://sz.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=113205000141492526332010502800201&ql_kind=01&iddept_ql_inf=1132050001414925263320105028002", 
            "材料名称": "申请主体资格证书",
            "元素名称": "空白表格",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        },
        {
            "序号": 10,
            "事项类型": "事项巡检",
            "事项名称": "江苏省新型冠状病毒肺炎疫情防控", 
            "检测类型": "事项巡检",
            "url": "https://sz.jszwfw.gov.cn/jszwfw/bscx/itemlist/bszn.do?webId=3&iddept_yw_inf=113205000141492526332010502800201&ql_kind=01&iddept_ql_inf=1132050001414925263320105028002",
            "材料名称": "申请主体资格证书", 
            "元素名称": "示例样表",
            "元素类型": "下载链接",
            "执行方式": "playwright",
            "执行时间": "",
            "执行结果": ""
        }
    ]
    
    # 创建DataFrame
    df = pd.DataFrame(test_data)
    
    # 保存为Excel文件
    output_file = "sample_test_data.xlsx"
    df.to_excel(output_file, index=False)
    
    print(f"✅ 示例测试数据已创建: {output_file}")
    print(f"📊 数据包含 {len(df)} 行测试用例")
    print("\n🔍 数据预览:")
    print(df[['序号', '材料名称', '元素名称', 'url']].head())
    
    return output_file

if __name__ == "__main__":
    create_sample_data()
