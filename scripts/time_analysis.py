"""
地震数据统计器 - 时间维度分析
功能：分析地震在星期几和一天中哪个时段最活跃
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体，防止图表乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 确保输出文件夹存在
if not os.path.exists('../output/images'):
    os.makedirs('../output/images')

print("=" * 60)
print("📊 地震数据统计器 - 时间维度分析")
print("=" * 60)

# 1. 加载数据
print("\n📂 正在加载数据...")
df = pd.read_csv('../data/earthquakes_raw.csv')
print(f"✅ 已加载 {len(df)} 条地震记录")

# 2. 将“时间”列转换为 datetime 格式，方便提取信息
df['时间'] = pd.to_datetime(df['时间'])

# 3. 提取时间特征
# 提取“星期几”：Monday=0, Sunday=6
df['星期'] = df['时间'].dt.dayofweek
# 提取“小时”：0-23
df['小时'] = df['时间'].dt.hour

# 4. 将“星期几”的数字转换为中文名称，方便阅读
weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
df['星期名称'] = df['星期'].map(weekday_map)

print("\n✅ 时间特征提取完成！")
print(f"📅 数据时间范围: {df['时间'].min()} 至 {df['时间'].max()}")
print(f"📊 包含的星期: {df['星期名称'].unique().tolist()}")

# 5. 分析：按星期统计地震次数
print("\n📊 按星期统计地震次数：")
weekly_counts = df['星期名称'].value_counts().reindex(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
print(weekly_counts)

# 6. 分析：按小时统计地震次数
print("\n📊 按小时统计地震次数（前5个时段）：")
hourly_counts = df['小时'].value_counts().sort_index()
print(hourly_counts.head(10))

# 7. 可视化
print("\n📈 正在生成时间分析图表...")

# 图1：星期分布柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=weekly_counts.index, y=weekly_counts.values, palette='viridis')
plt.title('一周内各天的地震发生次数', fontsize=16, fontweight='bold')
plt.xlabel('星期', fontsize=12)
plt.ylabel('地震次数', fontsize=12)
for i, v in enumerate(weekly_counts.values):
    plt.text(i, v + 5, str(v), ha='center', fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../output/images/weekly_distribution.png', dpi=150)
plt.show()
print("   ✅ 已保存: output/images/weekly_distribution.png")

# 图2：小时分布柱状图
plt.figure(figsize=(14, 6))
sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette='coolwarm')
plt.title('一天内各时段的地震发生次数', fontsize=16, fontweight='bold')
plt.xlabel('小时 (0-23)', fontsize=12)
plt.ylabel('地震次数', fontsize=12)
plt.xticks(range(0, 24))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../output/images/hourly_distribution.png', dpi=150)
plt.show()
print("   ✅ 已保存: output/images/hourly_distribution.png")

# 8. 简单结论
print("\n" + "=" * 60)
print("📋 分析结论")
print("=" * 60)

# 找出地震最多的星期
busiest_day = weekly_counts.idxmax()
busiest_day_count = weekly_counts.max()
print(f"📅 地震最多的星期: {busiest_day} ({busiest_day_count} 次)")

# 找出地震最少的一天
quietest_day = weekly_counts.idxmin()
quietest_day_count = weekly_counts.min()
print(f"📅 地震最少的星期: {quietest_day} ({quietest_day_count} 次)")

# 找出地震最多的时段
busiest_hour = hourly_counts.idxmax()
busiest_hour_count = hourly_counts.max()
print(f"⏰ 地震最多的时段: {busiest_hour}:00 ({busiest_hour_count} 次)")

print("\n✅ 时间维度分析完成！")