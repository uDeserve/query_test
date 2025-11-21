import os
import openai
import base64
from openai import OpenAI

model_id = "gpt-4o"
prompt_path = "english_prompt.txt"
image_directory = "my_images_frequency"
run_count_file = "run_count.txt"  # 定义存储运行次数的文件

# 读取当前运行次数
if os.path.exists(run_count_file):
    with open(run_count_file, "r") as f:
        run_count = int(f.read().strip())  # 读取现有的运行次数
else:
    run_count = 0  # 如果文件不存在，则从0开始

run_count += 1  # 增加运行次数

# 将当前运行次数写回文件
with open(run_count_file, "w") as f:
    f.write(str(run_count))

# 定义函数将图像文件转换为 Base64 编码字符串
def image_to_base64(image_path):
    # 读取图像文件并将其转换为 Base64 编码字符串
    with open(image_path, "rb") as image_file:
        # 读取图像文件的二进制内容
        image_data = image_file.read()
        # 将二进制数据转换为 Base64 编码
        base64_encoded_data = base64.b64encode(image_data)
        # 将编码后的数据从字节串转换为字符串
        base64_string = base64_encoded_data.decode('utf-8')
        return base64_string


# 设置API密钥
client = OpenAI(
    api_key=""
)
# 读取文本内容
with open(prompt_path, "r", encoding="utf-8") as text_file:
    text_content = text_file.read().strip()

# 获取图像目录下的所有文件

image_files = [f for f in os.listdir(image_directory) if "spectrum" in f and f.endswith(('.png', '.jpg', '.jpeg'))]

file_name_info = {}
output_info = {}
results = []
# 依次处理每个图像文件
for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    img_b64_str = image_to_base64(image_path)
    img_type = "image/jpeg" if image_file.endswith(".jpg") or image_file.endswith(".jpeg") else "image/png"
    # 调用 API 接口生成响应
    # 获取文件名
    file_name = os.path.basename(image_path)

    # 检查文件名中是否包含“left”或“right”
    if "left" in file_name.lower():
        file_name_info[file_name] = "left"
    elif "right" in file_name.lower():
        file_name_info[file_name] = "right"
    else:
        file_name_info[file_name] = "unknown"

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_content},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"},
                        },
                    ],
            }
        ],
    )
    # 打印响应
    response_content = response.choices[0].message.content
    # 在response内容中查找“左”和“右”出现的索引
    left_index = response_content.rfind("left")
    right_index = response_content.rfind("right")

    # 判断哪个字的索引更小，更新output_info中的key值
    if left_index != -1 and (right_index == -1 or left_index < right_index):
        output_info[file_name] = "right"
    elif right_index != -1:
        output_info[file_name] = "left"
    else:
        output_info[file_name] = "unknown"  # 如果都没找到，标记为unknown
    # 写入到文件
    # 生成基于run_count的文件名

    # 比较output_info和file_name_info
    if output_info.get(file_name) == file_name_info[file_name]:
        results.append(True)  # 结果正确
    else:
        results.append(False)  # 结果错误

    output_filename = f'output_run_{run_count}.txt'
    # 打开以run_count命名的文件进行写入

    with open(output_filename, 'a') as f:  # 'a'模式是追加写入
        output_content = f"Run Count: {run_count}\n Model: {model_id}\nImage_directory: {image_directory}\n Image: {image_file}\n Query: {text_content},\n Response: {response_content}\nImage Type: {file_name_info[file_name]}\nGPT_judge: {output_info[file_name]}\nJudgment results: {results[len(results) - 1]}\n\n"
        # 打印响应到控制台
        print(output_content)

        # 同时写入到文件
        f.write(output_content)
        f.write("\n")
        # 打印文件名信息



# 计算正确率
correct_count = sum(results)  # 计算True的数量
total_queries = len(results)  # 查询总数
accuracy = correct_count / total_queries if total_queries > 0 else 0  # 防止除以零

# 输出正确率
with open(output_filename, 'a') as f:  # 'a'模式是追加写入
    f.write(f"查询正确率: {accuracy * 100:.2f}%\n")


print(f"查询正确率: {accuracy * 100:.2f}%")
