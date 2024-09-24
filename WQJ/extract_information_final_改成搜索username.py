# 1.10重新提取json中的数据

import json
import pandas as pd
import os
import glob
import json


def find_screen_name_id_in_directory(directory, target_screen_name):
    all_files = glob.glob(os.path.join(directory, '**/*.txt'), recursive=True)
    all_line = 0
    found_id = None

    for input_file in all_files:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                all_line += 1
                if all_line % 50000 == 0:
                    print(f"{input_file} 处理到行数: {all_line}（当i是50000的倍数时才输出）")

                obj = json.loads(line)
                user = obj.get('user', {})
                screen_name = user.get('screen_name', None)

                if screen_name == target_screen_name:
                    found_id = user.get('id_str', None)
                    print(f"找到screen_name为'{target_screen_name}'的id: {found_id}，文件: {input_file}")
                    return found_id  # 找到目标后立即返回

    print(f"未找到screen_name为'{target_screen_name}'的用户")
    return found_id



if __name__ == "__main__":
    # 调用示例
    directory = 'F:\\us-presidential'
    target_screen_name = 'nowthisnews'
    found_id = find_screen_name_id_in_directory(directory, target_screen_name)

    if found_id:
        print(f"screen_name为'{target_screen_name}'的用户id为: {found_id}")
    else:
        print(f"未找到screen_name为'{target_screen_name}'的用户")
