"""
地震数据统计器 - 地震查询与地图展示
功能：按震级筛选地震，并在地图上显示位置
"""

import pandas as pd
import folium
from folium import plugins
from IPython.display import display
import webbrowser
import tempfile
import os

print("=" * 60)
print("🌍 地震数据统计器 - 地震查询与地图展示")
print("=" * 60)

# 1. 加载数据
print("\n📂 正在加载数据...")
df = pd.read_csv('../data/earthquakes_raw.csv')
print(f"✅ 已加载 {len(df)} 条地震记录")

# 2. 显示数据范围
print(f"\n📊 震级范围: {df['震级'].min():.1f} 至 {df['震级'].max():.1f}")

# 3. 用户输入查询条件
print("\n" + "=" * 60)
print("🔍 地震查询")
print("=" * 60)

print("\n请选择查询方式：")
print("1️⃣ 按震级查询（如：输入 5.0，查询震级 >= 5.0 的地震）")
print("2️⃣ 按震级区间查询（如：输入 4.0-6.0，查询震级在 4.0 到 6.0 之间的地震）")
print("3️⃣ 按地点关键词查询（如：输入 'Japan'，查询地点包含 Japan 的地震）")

choice = input("\n请输入选项 (1/2/3): ").strip()

# 4. 根据用户选择筛选数据
filtered_df = df.copy()

if choice == '1':
    try:
        mag = float(input("请输入震级阈值（如 5.0）: "))
        filtered_df = df[df['震级'] >= mag]
        print(f"\n✅ 查询到震级 >= {mag} 的地震 {len(filtered_df)} 条")
    except ValueError:
        print("❌ 输入格式错误，请输入数字")
        exit()

elif choice == '2':
    try:
        parts = input("请输入震级区间（如 4.0-6.0）: ").split('-')
        min_mag = float(parts[0].strip())
        max_mag = float(parts[1].strip())
        filtered_df = df[(df['震级'] >= min_mag) & (df['震级'] <= max_mag)]
        print(f"\n✅ 查询到震级在 {min_mag} 至 {max_mag} 之间的地震 {len(filtered_df)} 条")
    except (ValueError, IndexError):
        print("❌ 输入格式错误，请输入 震级下限-震级上限（如 4.0-6.0）")
        exit()

elif choice == '3':
    keyword = input("请输入地点关键词（如 Japan）: ").strip()
    filtered_df = df[df['地点'].str.contains(keyword, case=False, na=False)]
    print(f"\n✅ 查询到地点包含 '{keyword}' 的地震 {len(filtered_df)} 条")

else:
    print("❌ 无效选项")
    exit()

# 5. 显示查询结果
if len(filtered_df) == 0:
    print("\n😅 没有找到符合条件的地震记录")
    exit()

print("\n" + "=" * 60)
print("📋 查询结果")
print("=" * 60)

# 显示数据统计
print(f"\n📊 震级统计:")
print(f"   - 最大: {filtered_df['震级'].max():.1f}")
print(f"   - 最小: {filtered_df['震级'].min():.1f}")
print(f"   - 平均: {filtered_df['震级'].mean():.2f}")

print(f"\n📊 深度统计:")
print(f"   - 最深: {filtered_df['深度(km)'].max():.1f} km")
print(f"   - 最浅: {filtered_df['深度(km)'].min():.1f} km")

# 显示前10条数据
print(f"\n📋 前10条记录:")
print("=" * 80)
display_df = filtered_df[['时间', '震级', '深度(km)', '地点']].head(10)
print(display_df.to_string(index=False))
print("=" * 80)

# 6. 询问是否生成地图
show_map = input("\n🗺️ 是否生成地震位置地图？(y/n): ").strip().lower()

if show_map == 'y':
    print("\n🗺️ 正在生成地图...")
    
    # 计算地图中心（取所有点的平均经纬度）
    center_lat = filtered_df['纬度'].mean()
    center_lon = filtered_df['经度'].mean()
    
    # 创建地图
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2, tiles='OpenStreetMap', attr='OpenStreetMap contributors')
    
    # 添加地震标记
    for idx, row in filtered_df.iterrows():
        # 根据震级大小决定标记颜色和大小
        mag = row['震级']
        if mag >= 6.0:
            color = 'red'
            radius = 15
            popup_color = 'darkred'
        elif mag >= 5.0:
            color = 'orange'
            radius = 12
            popup_color = 'orange'
        elif mag >= 4.0:
            color = 'yellow'
            radius = 9
            popup_color = 'gold'
        else:
            color = 'green'
            radius = 6
            popup_color = 'green'
        
        # 弹出信息
        popup_text = f"""
        <b>地点:</b> {row['地点']}<br>
        <b>震级:</b> {row['震级']:.1f}<br>
        <b>深度:</b> {row['深度(km)']:.1f} km<br>
        <b>时间:</b> {row['时间']}
        """
        
        folium.CircleMarker(
            location=[row['纬度'], row['经度']],
            radius=radius,
            popup=folium.Popup(popup_text, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=2
        ).add_to(m)
    
    # 添加图例
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; 
                width: 150px; height: 120px; 
                border:2px solid grey; 
                background-color: white;
                z-index:9999; 
                font-size:12px;
                padding: 10px;">
        <b>震级</b><br>
        <span style="color: red;">●</span> ≥ 6.0<br>
        <span style="color: orange;">●</span> 5.0 - 5.9<br>
        <span style="color: yellow;">●</span> 4.0 - 4.9<br>
        <span style="color: green;">●</span> 2.5 - 3.9
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # 添加聚类功能（当标记太多时）
    marker_cluster = plugins.MarkerCluster().add_to(m)
    for idx, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['纬度'], row['经度']],
            popup=f"{row['地点']}<br>震级: {row['震级']:.1f}",
            icon=folium.Icon(color='red' if row['震级'] >= 6 else 'orange' if row['震级'] >= 5 else 'green')
        ).add_to(marker_cluster)
    
    # 保存地图到临时文件并自动打开
    map_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    m.save(map_file.name)
    print(f"\n✅ 地图已生成！")
    print(f"📁 地图文件: {map_file.name}")
    
    # 自动在浏览器中打开
    webbrowser.open('file://' + map_file.name)
    print("🌐 已在浏览器中打开地图")

print("\n✅ 查询完成！")