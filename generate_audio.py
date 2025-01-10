import os
import pandas as pd
import asyncio
from edge_tts import Communicate

# 定义音频保存目录
audio_dir = "audio_files"
os.makedirs(audio_dir, exist_ok=True)  # 如果目录不存在则创建

# 定义音频生成函数
async def generate_audio(word, output_path):
    try:
        # 使用女性芬兰语语音
        communicate = Communicate(text=word, voice="fi-FI-NooraNeural")
        await communicate.save(output_path)  # 保存音频到指定路径
    except Exception as e:
        print(f"生成音频时出错：{word}, 错误信息：{e}")

# 递归查找所有 Excel 文件
def find_excel_files(base_dir):
    excel_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".xlsx"):  # 查找以 .xlsx 结尾的文件
                excel_files.append(os.path.join(root, file))
    return excel_files

# 处理单个 Excel 文件并保持层级结构
def process_excel(file_path, base_dir):
    print(f"正在处理文件：{file_path}")
    df = pd.read_excel(file_path, header=None)  # 假设单词在第一列
    finnish_words = df[0].dropna().unique()  # 去除空值并获取唯一单词

    # 根据文件路径创建层级结构
    relative_path = os.path.relpath(file_path, base_dir)  # 计算相对路径
    sub_dir = os.path.dirname(relative_path)  # 获取子目录路径

    for word in finnish_words:
        word = word.strip()
        # 在保存目录中保留子目录层级
        output_sub_dir = os.path.join(audio_dir, sub_dir)
        os.makedirs(output_sub_dir, exist_ok=True)  # 创建子目录

        output_file = os.path.join(output_sub_dir, f"{word}.mp3")
        if not os.path.exists(output_file):  # 避免重复生成音频
            print(f"正在生成音频：{word}")
            asyncio.run(generate_audio(word, output_file))
        else:
            print(f"音频已存在：{word}")

# 主函数：递归处理所有 Excel 文件
if __name__ == "__main__":
    # GitHub 本地存储路径
    base_dir = r"D:\finnish-space"  # 替换为你的实际路径
    excel_files = find_excel_files(base_dir)  # 查找所有 Excel 文件
    
    for excel_file in excel_files:
        process_excel(excel_file, base_dir)  # 处理每个 Excel 文件
    
    print("所有音频已生成完毕！")
