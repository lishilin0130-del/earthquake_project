"""
地震数据统计器 - 数据获取模块
功能：从USGS获取最近30天的地震数据
"""

import pandas as pd
import requests
from datetime import datetime, timedelta

print("=" * 60)
print("🌍 地震数据统计器 - 数据获取")
print("=" * 60)

# 1. 从USGS获取地震数据
print("\n📡 正在连接USGS地震数据库...")

# USGS地震数据API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# 查询参数
params = {
    "format": "geojson",
    "starttime": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
    "endtime": datetime.now().strftime("%Y-%m-%d"),
    "minmagnitude": 2.5,      # 最小震级2.5
    "orderby": "time"
}

try:
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    print(f"✅ 成功获取 {len(data['features'])} 条地震记录")
except Exception as e:
    print(f"❌ 数据获取失败: {e}")
    exit()

# 2. 解析数据
print("\n📊 正在解析数据...")

records = []
for feature in data['features']:
    props = feature['properties']
    geom = feature['geometry']['coordinates']
    
    # 提取字段
    mag = props.get('mag', None)
    place = props.get('place', '未知地点')
    time_ms = props.get('time', 0)
    
    # 时间转换：毫秒 → 可读日期
    time_str = datetime.fromtimestamp(time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    
    # 经纬度、深度 (经度, 纬度, 深度)
    lon, lat, depth = geom[0], geom[1], geom[2]
    
    records.append({
        '时间': time_str,
        '纬度': round(lat, 4),
        '经度': round(lon, 4),
        '深度(km)': round(depth, 2),
        '震级': mag,
        '地点': place
    })

# 3. 转换为DataFrame并保存
df = pd.DataFrame(records)

# 过滤掉震级为空的数据
df = df[df['震级'].notna()]
print(f"✅ 有效数据: {len(df)} 条")

# 保存为CSV
df.to_csv('../data/earthquakes_raw.csv', index=False, encoding='utf-8-sig')
print(f"💾 数据已保存到 earthquakes_raw.csv")

# 4. 数据概览
print("\n" + "=" * 60)
print("📋 数据概览")
print("=" * 60)
print(f"📅 时间范围: {df['时间'].min()} 至 {df['时间'].max()}")
print(f"📊 总记录数: {len(df)}")
print(f"⭐ 最大震级: {df['震级'].max():.1f}")
print(f"⭐ 最小震级: {df['震级'].min():.1f}")
print(f"📈 平均震级: {df['震级'].mean():.2f}")
print(f"📉 最深地震: {df['深度(km)'].max():.1f} km")
print(f"📈 最浅地震: {df['深度(km)'].min():.1f} km")

print("\n📋 前5条数据预览:")
print(df.head().to_string())

print("\n✅ 数据获取完成！")