# ImageWithMessage 使用说明

## 简介

`ImageWithMessage` 是一个 Python 类，用于结合图像文件和自定义消息，利用 `qianfan` API 进行图像分析。

## 依赖

- Python 3.x
- `qianfan` 库

安装命令：

```bash
pip install qianfan

##环境变量配置
###在运行代码前，设置环境变量：
os.environ["QIANFAN_ACCESS_KEY"] = "your_iam_ak"
os.environ["QIANFAN_SECRET_KEY"] = "your_iam_sk"

##使用方法
###示例代码
```if __name__ == '__main__':
    image_folder = "images"  # 图像文件夹路径
    message_path = "message2.txt"  # 消息文件路径
    model = "Fuyu-8B"  # 模型名称
    query_num = 2  # 查询数量
    message_use = True  # 是否使用消息文件
    
    image_query = ImageWithMessage(image_folder, message_path, query_num, model, message_use)
    results = image_query.do_query()
    
    for result in results:
        print(result)```

##输入格式
###图像文件夹: 包含图像文件（.jpg, .jpeg, .png, .bmp）。
###消息文件: 包含用于分析的提示消息的文本文件。

##输出
控制台将输出每张图像的分析结果。
