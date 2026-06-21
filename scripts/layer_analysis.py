"""
地震数据统计器 - 震级分层验证
功能：将地震按大小分组，验证“周六/8点效应”是否真实存在
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 确保输出文件夹存在
if not os.path.exists('../output/images'):
    os.makedirs('../output/images')

print("=" * 60)
print("🔬 地震数据统计器 - 震级分层验证")
print("=" * 60)

# 1. 加载数据
print("\n📂 正在加载数据...")
df = pd.read_csv('../data/earthquakes_raw.csv')
df['时间'] = pd.to_datetime(df['时间'])
print(f"✅ 已加载 {len(df)} 条地震记录")

# 2. 定义分组标准：震级小于 4.5 级的算“小地震”，>= 4.5 级的算“大地震”
# （为什么要选4.5？因为4.5级是一个比较常用的分界点，它代表“可能被感觉到”的门槛）
mag_threshold = 4.5
df['震级分组'] = df['震级'].apply(lambda x: '大地震' if x >= mag_threshold else '小地震')

print(f"\n📊 震级分布：")
print(f"   - 大地震 (≥ {mag_threshold}级): {len(df[df['震级分组'] == '大地震'])} 条")
print(f"   - 小地震 (< {mag_threshold}级): {len(df[df['震级分组'] == '小地震'])} 条")

# 3. 提取“星期”信息
weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
df['星期'] = df['时间'].dt.dayofweek
df['星期名称'] = df['星期'].map(weekday_map)

# 4. 分别统计两组数据的“星期分布”
weekly_counts_all = df['星期名称'].value_counts().reindex(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
weekly_counts_small = df[df['震级分组'] == '小地震']['星期名称'].value_counts().reindex(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
weekly_counts_large = df[df['震级分组'] == '大地震']['星期名称'].value_counts().reindex(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])

# 5. 打印结果进行对比
print("\n📅 不同震级组的一周分布对比：")
print("-" * 40)
print(f"{'星期':<6} {'全部地震':<10} {'小地震':<10} {'大地震':<10}")
for day in ['周一', '周二', '周三', '周四', '周五', '周六', '周日']:
    all_count = weekly_counts_all.get(day, 0)
    small_count = weekly_counts_small.get(day, 0)
    large_count = weekly_counts_large.get(day, 0)
    print(f"{day:<6} {all_count:<10} {small_count:<10} {large_count:<10}")

# 6. 可视化对比（并排柱状图）
print("\n📈 正在生成对比图表...")

# 准备对比数据
compare_df = pd.DataFrame({
    '小地震': weekly_counts_small,
    '大地震': weekly_counts_large
}).fillna(0)  # 把空值替换为0

# 绘制并排柱状图
fig, ax = plt.subplots(figsize=(14, 7))
compare_df.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c'], alpha=0.7)
ax.set_title('不同震级地震的一周分布对比', fontsize=16, fontweight='bold')
ax.set_xlabel('星期', fontsize=12)
ax.set_ylabel('地震次数', fontsize=12)
ax.legend(['小地震 (< 4.5级)', '大地震 (≥ 4.5级)'])
ax.grid(axis='y', alpha=0.3)

# 在柱子上添加数值标签
for container in ax.containers:
    ax.bar_label(container, label_type='edge', fontsize=9)

plt.tight_layout()
plt.savefig('../output/images/layer_comparison.png', dpi=150)
plt.show()

print("   ✅ 已保存: output/images/layer_comparison.png")

# 7. 简单结论
print("\n" + "=" * 60)
print("📋 验证结论")
print("=" * 60)

# 找出小地震组中地震最多的星期
small_busiest = weekly_counts_small.idxmax()
small_busiest_count = weekly_counts_small.max()
print(f"🔹 小地震最多的星期: {small_busiest} ({small_busiest_count} 次)")

# 找出大地震组中地震最多的星期
large_busiest = weekly_counts_large.idxmax()
large_busiest_count = weekly_counts_large.max()
print(f"🔸 大地震最多的星期: {large_busiest} ({large_busiest_count} 次)")

print("\n💡 初步判断：")
if small_busiest == '周六' and large_busiest != '周六':
    print("   ✅ 周六效应主要出现在小地震中，支持'观测偏差'的假设。")
elif small_busiest == '周六' and large_busiest == '周六':
    print("   ⚠️ 周六效应在大小地震中都出现，可能反映了真实的物理规律。")
else:
    print("   🤔 结果模式不明确，可能需要更长时间的数据来分析。")

print("\n✅ 震级分层验证完成！")