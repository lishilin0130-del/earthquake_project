"""
项目文件整理工具
自动创建文件夹结构，移动文件，并更新代码中的路径
"""

import os
import shutil
import re
from pathlib import Path

print("=" * 60)
print("📁 地震项目 - 文件整理工具")
print("=" * 60)

# 项目根目录
root_dir = Path.cwd()
print(f"\n📂 当前目录: {root_dir}")

# 1. 创建文件夹结构
print("\n📁 正在创建文件夹结构...")

folders = [
    'data',
    'scripts',
    'output/images'
]

for folder in folders:
    folder_path = root_dir / folder
    if not folder_path.exists():
        folder_path.mkdir(parents=True)
        print(f"   ✅ 创建: {folder}")
    else:
        print(f"   ⏭️ 已存在: {folder}")

# 2. 移动文件
print("\n📦 正在移动文件...")

# 定义要移动的文件： (源文件, 目标文件夹)
file_moves = [
    ('earthquakes_raw.csv', 'data/earthquakes_raw.csv'),
    ('get_data.py', 'scripts/get_data.py'),
    ('analyze_data.py', 'scripts/analyze_data.py'),
    ('query_earthquakes.py', 'scripts/query_earthquakes.py'),
]

# 如果 images 文件夹存在，移到 output 下
if (root_dir / 'images').exists() and not (root_dir / 'output/images').exists():
    shutil.move(str(root_dir / 'images'), str(root_dir / 'output/images'))
    print("   ✅ 移动: images/ → output/images/")

for src, dst in file_moves:
    src_path = root_dir / src
    dst_path = root_dir / dst
    
    if src_path.exists():
        # 确保目标文件夹存在
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        # 如果目标文件已存在，先删除
        if dst_path.exists():
            dst_path.unlink()
        # 移动文件
        shutil.move(str(src_path), str(dst_path))
        print(f"   ✅ 移动: {src} → {dst}")
    else:
        print(f"   ⏭️ 跳过: {src} (不存在)")

# 3. 更新代码中的文件路径
print("\n🔧 正在更新代码路径...")

# 需要更新的文件
script_files = [
    'scripts/get_data.py',
    'scripts/analyze_data.py',
    'scripts/query_earthquakes.py'
]

for script in script_files:
    script_path = root_dir / script
    if not script_path.exists():
        print(f"   ⏭️ 跳过: {script} (不存在)")
        continue
    
    # 读取文件内容
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 替换路径（根据不同文件）
    if 'get_data.py' in script:
        # 保存CSV的路径
        content = content.replace(
            "df.to_csv('earthquakes_raw.csv'",
            "df.to_csv('../data/earthquakes_raw.csv'"
        )
        content = content.replace(
            'df.to_csv("earthquakes_raw.csv"',
            'df.to_csv("../data/earthquakes_raw.csv"'
        )
    
    elif 'analyze_data.py' in script:
        # 读取CSV的路径
        content = content.replace(
            "pd.read_csv('earthquakes_raw.csv')",
            "pd.read_csv('../data/earthquakes_raw.csv')"
        )
        content = content.replace(
            'pd.read_csv("earthquakes_raw.csv")',
            'pd.read_csv("../data/earthquakes_raw.csv")'
        )
        # 保存图片的路径
        content = content.replace(
            "plt.savefig('images/",
            "plt.savefig('../output/images/"
        )
        content = content.replace(
            'plt.savefig("images/',
            'plt.savefig("../output/images/'
        )
        # 创建images文件夹（改为在output下）
        content = content.replace(
            "if not os.path.exists('images'):",
            "if not os.path.exists('../output/images'):"
        )
        content = content.replace(
            "os.makedirs('images')",
            "os.makedirs('../output/images')"
        )
    
    elif 'query_earthquakes.py' in script:
        # 读取CSV的路径
        content = content.replace(
            "pd.read_csv('earthquakes_raw.csv')",
            "pd.read_csv('../data/earthquakes_raw.csv')"
        )
        content = content.replace(
            'pd.read_csv("earthquakes_raw.csv")',
            'pd.read_csv("../data/earthquakes_raw.csv")'
        )
    
    # 如果内容有变化，写回文件
    if content != original_content:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ 更新: {script}")
    else:
        print(f"   ⏭️ 无需更新: {script}")

# 4. 生成新的 requirements.txt（包含新依赖）
print("\n📋 正在更新 requirements.txt...")

requirements_content = """pandas>=1.5.0
numpy>=1.24.0
requests>=2.28.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.2.0
folium>=0.14.0
ipython>=8.0.0
"""

req_path = root_dir / 'requirements.txt'
with open(req_path, 'w', encoding='utf-8') as f:
    f.write(requirements_content)
print("   ✅ 已更新 requirements.txt")

# 5. 显示最终结构
print("\n" + "=" * 60)
print("✅ 整理完成！")
print("=" * 60)

print("\n📂 新的项目结构:")
print("""
EARTHQUAKE_PROJECT/
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── data/
│   └── earthquakes_raw.csv          ← 数据文件
├── scripts/
│   ├── get_data.py                  ← 数据获取
│   ├── analyze_data.py              ← 数据分析
│   └── query_earthquakes.py         ← 地震查询
└── output/
    └── images/                      ← 图表输出
""")

print("\n📌 使用说明:")
print("   cd scripts")
print("   python get_data.py")
print("   python analyze_data.py")
print("   python query_earthquakes.py")

print("\n🚀 整理完成！可以开始使用新的项目结构了。")