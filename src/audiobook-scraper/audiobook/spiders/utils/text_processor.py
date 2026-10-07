import re
from pathlib import Path


class TextProcessor:
    @staticmethod
    def clean(content):
        text = "".join(content)
        # 1. 移除特殊空白
        text = text.replace("\u2003", "")

        # 2. 處理每一行
        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        # 3. 移除空白行
        lines = [
            line
            for line in lines
            if line
        ]

        # 4. 合併文字
        text = "\n".join(lines)

        return text

    def export_txt(self, output_dir, filename, content):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / f"{filename}.txt"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"TXT 已輸出：{file_path}")
