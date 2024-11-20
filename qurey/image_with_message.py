import os
import qianfan
import base64
from qianfan.resources import Image2Text

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk

os.environ["QIANFAN_ACCESS_KEY"] = "0a41bf2198f84c1ea79227e19a5a44e4"
os.environ["QIANFAN_SECRET_KEY"] = "496b882a10bb44e6aa8633da300cfbd0"


class ImageWithMessage:
    def __init__(self, image_folder, message_path, query_num, model, message_use):
        self.image_folder = image_folder
        self.message_path = message_path
        self.query_num = query_num
        self.model = model
        self.image_paths = self.get_image_paths()

    def get_image_paths(self):
        # 获取文件夹中所有图像文件
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
        return [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if
                f.endswith(valid_extensions)]

    def do_query(self):
        i2t = Image2Text(model=self.model)
        results = []
        message = None
        with open(self.message_path, "r", encoding="utf-8") as f:
            message = f.read()
        # 遍历每个图像路径并进行处理
        for i in range(min(self.query_num, len(self.image_paths))):  # 确保不超出图像数量
            with open(self.image_paths[i], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            if message_use == False:
                prompt = "分析一下图片画了什么？"  # 手动更改prompt
            else:
                prompt = message  # 文件读取prompt

            # 调用 API 进行图像分析
            resp = i2t.do(prompt=prompt, image=encoded_string)
            results.append(resp["result"])

        return results


# 使用示例
if __name__ == '__main__':
    image_folder = "images"  # 替换为您的图像文件夹路径
    message_path = "message2.txt"  # 替换为您的消息文件路径
    model = "Fuyu-8B"
    query_num = 2  # 读取的图像数量
    message_use = True  # 是否使用文件读取的消息
    image_query = ImageWithMessage(image_folder=image_folder, message_path=message_path, query_num=query_num,
                                   model=model, message_use=message_use)
    results = image_query.do_query()

    for result in results:
        print("\n")
        print(result)
