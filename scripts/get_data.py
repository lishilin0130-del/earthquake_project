"""
地震数据统计器 - 数据获取模块（支持长时间范围）
功能：从USGS获取地震数据，支持超过30天的长时间范围
"""

import pandas as pd
import requests
from datetime import datetime, timedelta
import time

print("=" * 60)
print("🌍 地震数据统计器 - 数据获取（分段版）")
print("=" * 60)

# ============================================================
# 配置参数
# ============================================================
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# 用户配置
total_days = 365  # 要获取的总天数
min_magnitude = 2.5  # 最小震级
segment_days = 30  # 每次获取的天数（30天最稳定）

print(f"\n📋 配置信息:")
print(f"   - 总天数: {total_days} 天")
print(f"   - 最小震级: {min_magnitude}")
print(f"   - 每段天数: {segment_days} 天")

# ============================================================
# 分段获取数据
# ============================================================
print("\n📡 正在分段获取数据...")

all_records = []
end_date = datetime.now()
start_date = end_date - timedelta(days=total_days)

# 计算需要分多少段
num_segments = (total_days + segment_days - 1) // segment_days
print(f"📊 共需 {num_segments} 次请求")

for i in range(num_segments):
    # 计算当前段的起止时间
    segment_end = end_date - timedelta(days=i * segment_days)
    segment_start = segment_end - timedelta(days=segment_days)
    
    # 如果 segment_start 早于 start_date，则从 start_date 开始
    if segment_start < start_date:
        segment_start = start_date
    
    print(f"\n   📡 第 {i+1}/{num_segments} 段: {segment_start.strftime('%Y-%m-%d')} → {segment_end.strftime('%Y-%m-%d')}")
    
    params = {
        "format": "geojson",
        "starttime": segment_start.strftime("%Y-%m-%d"),
        "endtime": segment_end.strftime("%Y-%m-%d"),
        "minmagnitude": min_magnitude,
        "orderby": "time"
    }

    try:
        response = requests.get(url, params=params, timeout=60)
        data = response.json()
        features = data.get('features', [])
        print(f"      ✅ 获取到 {len(features)} 条记录")

        # 解析数据
        for feature in features:
            props = feature['properties']
            geom = feature['geometry']['coordinates']
            mag = props.get('mag', None)
            if mag is None or mag < min_magnitude:
                continue

            all_records.append({
                '时间': datetime.fromtimestamp(props.get('time', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                '纬度': round(geom[1], 4),
                '经度': round(geom[0], 4),
                '深度(km)': round(geom[2], 2),
                '震级': mag,
                '地点': props.get('place', '未知地点')
            })

        # 避免请求过快
        time.sleep(0.5)

    except Exception as e:
        print(f"      ❌ 获取失败: {e}")
        continue

# ============================================================
# 保存数据
# ============================================================
print("\n" + "=" * 60)
print("📊 数据汇总")
print("=" * 60)

df = pd.DataFrame(all_records)
print(f"✅ 总共获取 {len(df)} 条地震记录")

if not df.empty:
    # 去重（按时间、经纬度、震级去重）
    df = df.drop_duplicates(subset=['时间', '纬度', '经度', '震级'])
    print(f"✅ 去重后剩余 {len(df)} 条记录")

    # 保存
    df.to_csv('../data/earthquakes_raw.csv', index=False, encoding='utf-8-sig')
    print(f"💾 数据已保存到 earthquakes_raw.csv")

    # 数据概览
    print(f"\n📅 时间范围: {df['时间'].min()} 至 {df['时间'].max()}")
    print(f"⭐ 最大震级: {df['震级'].max():.1f}")
    print(f"⭐ 最小震级: {df['震级'].min():.1f}")
    print(f"📈 平均震级: {df['震级'].mean():.2f}")
else:
    print("❌ 没有获取到任何数据")

print("\n✅ 数据获取完成！")