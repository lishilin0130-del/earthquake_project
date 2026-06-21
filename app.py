"""
地震数据统计器 - 交互式网页应用
基于 Streamlit 框架，让数据分析变得可视化和可交互
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import requests
import urllib3

def get_region(lat, lon):
    if -35 <= lat <= 37 and -20 <= lon <= 52:
        return "非洲"
    if 8 <= lat <= 55 and 60 <= lon <= 150:
        return "亚洲"
    if 36 <= lat <= 70 and -10 <= lon <= 40:
        return "欧洲"
    if 15 <= lat <= 72 and -170 <= lon <= -55:
        return "北美洲"
    if -55 <= lat <= 15 and -82 <= lon <= -35:
        return "南美洲"
    if -40 <= lat <= -10 and 112 <= lon <= 155:
        return "大洋洲"
    if lat < -55:
        return "南极洲"
    return "其他海域"

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 👇 修复中文显示
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="🌍 地震数据统计器",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit as st

# ============================================================
# 页面配置（放在文件最前面）
# ============================================================
st.set_page_config(
    page_title="🌍 地震数据统计器",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 自定义 CSS 样式
# ============================================================
st.markdown("""
<style>
    /* 主色调：深蓝到深灰 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 侧边栏背景 */
    .css-1d391kg {
        background-color: #2c3e50;
    }
    
    /* 侧边栏文字颜色 */
    .css-1d391kg .stMarkdown, .css-1d391kg .stTextInput, .css-1d391kg .stSelectbox {
        color: #ecf0f1;
    }
    
    /* 标题样式 */
    h1 {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    
    /* 指标卡片样式 */
    .css-1y4p8pa {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    /* 按钮样式 */
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #2980b9;
        transform: scale(1.02);
    }
    
    /* 页脚样式 */
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 14px;
        padding: 20px 0;
        border-top: 1px solid #ddd;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 标题与说明
# ============================================================
st.title("🌍 地震数据统计器")
st.markdown("""
基于 USGS 数据的全球地震活动分析与可视化平台
""")

# ============================================================
# 侧边栏：数据加载与控制
# ============================================================
st.sidebar.header("⚙️ 控制面板")

# 数据加载方式选择
data_source = st.sidebar.radio(
    "📂 数据来源",
    ["📁 本地 CSV 文件", "📡 从 USGS 实时获取"]
)

@st.cache_data
def load_local_data():
    try:
        df = pd.read_csv('data/earthquakes_raw.csv')
        df['时间'] = pd.to_datetime(df['时间'])
        df['地区'] = df.apply(lambda row: get_region(row['纬度'], row['经度']), axis=1)
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def fetch_usgs_data(days=30, min_magnitude=2.5):
    """从 USGS API 获取数据"""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
        "endtime": datetime.now().strftime("%Y-%m-%d"),
        "minmagnitude": min_magnitude,
        "orderby": "time"
    }
    try:
        response = requests.get(url, params=params, timeout=60, verify=False)
        data = response.json()
        records = []
        for feature in data['features']:
            props = feature['properties']
            geom = feature['geometry']['coordinates']
            mag = props.get('mag', None)
            if mag is None or mag < min_magnitude:
                continue
            records.append({
                '时间': datetime.fromtimestamp(props.get('time', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                '纬度': round(geom[1], 4),
                '经度': round(geom[0], 4),
                '深度(km)': round(geom[2], 2),
                '震级': mag,
                '地点': props.get('place', '未知地点'),
                '地区': get_region(round(geom[1], 4), round(geom[0], 4))  # 👈 加这一行
            })
        df = pd.DataFrame(records)
        df['时间'] = pd.to_datetime(df['时间'])
        return df
    except Exception as e:
        st.error(f"数据获取失败: {e}")
        return None

# 在侧边栏底部添加“关于”部分
st.sidebar.markdown("---")
with st.sidebar.expander("📖 关于本项目"):
    st.markdown("""
    **🌍 地震数据统计器**
    
    基于 USGS 数据的全球地震活动分析与可视化平台。
    
    **📊 数据来源**
    - 美国地质调查局 (USGS) 地震目录 API
    
    **🔬 关键发现**
    - 周六地震最多 (635次)，周二最少 (524次)
    - “周六效应”主要出现在小地震中，支持“观测偏差”假说
    
    **🛠️ 技术栈**
    - Python + Streamlit
    - Pandas + Matplotlib + Seaborn
    - Folium 交互式地图
    
    **👤 作者**
    Shilin Li (lishilin0130-del)
    
    **📅 完成时间**
    2026年6月
    """)

# ============================================================
# 👇 关键修复：初始化 df
# ============================================================
df = None

# 加载数据
if data_source == "📁 本地 CSV 文件":
    df = load_local_data()
    if df is None:
        st.warning("未找到本地数据文件，请先运行 get_data.py 获取数据，或切换为实时获取")
        st.stop()
    st.sidebar.success(f"✅ 已加载 {len(df)} 条本地记录")
else:
    days = st.sidebar.slider("📅 查询天数", 1, 365, 30)
    min_mag = st.sidebar.slider("📊 最小震级", 0.0, 7.0, 2.5, 0.5)
    if st.sidebar.button("🔄 获取数据"):
        with st.spinner("正在从 USGS 获取数据..."):
            df = fetch_usgs_data(days, min_mag)
            if df is not None and not df.empty:
                st.sidebar.success(f"✅ 获取到 {len(df)} 条记录")
                # 保存到缓存
                df.to_csv('data/earthquakes_raw.csv', index=False)
            else:
                st.error("未获取到数据")
                st.stop()
    else:
        # 👇 关键修复：如果还没点击"获取数据"，用本地数据
        df = load_local_data()
        if df is None:
            st.warning("请先加载数据或点击'获取数据'按钮")
            st.stop()

if df is None or df.empty:
    st.warning("暂无数据，请先加载数据")
    st.stop()

# ============================================================
# 主界面：数据筛选与概览
# ============================================================
st.sidebar.header("🔍 数据筛选")

# 👇 添加地区筛选器（放在震级筛选之前）
region_options = ['🌍 全部'] + sorted(df['地区'].unique().tolist())
selected_region = st.sidebar.selectbox("📍 地区筛选", region_options)

# 筛选器
col1, col2, col3 = st.columns(3)
with col1:
    mag_min = st.slider("最低震级", float(df['震级'].min()), float(df['震级'].max()), float(df['震级'].min()), 0.5)
with col2:
    mag_max = st.slider("最高震级", float(df['震级'].min()), float(df['震级'].max()), float(df['震级'].max()), 0.5)
with col3:
    date_range = st.date_input(
        "日期范围",
        [df['时间'].min(), df['时间'].max()],
        min_value=df['时间'].min(),
        max_value=df['时间'].max()
    )

# 应用筛选
mask = (df['震级'] >= mag_min) & (df['震级'] <= mag_max)
if len(date_range) == 2:
    mask &= (df['时间'] >= pd.to_datetime(date_range[0])) & (df['时间'] <= pd.to_datetime(date_range[1]))

# 👇 应用地区筛选
if selected_region != '🌍 全部':
    mask &= (df['地区'] == selected_region)

filtered_df = df[mask]

# ============================================================
# 统计信息
# ============================================================
st.header("📊 数据概览")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📊 地震总数", len(filtered_df))
col2.metric("⭐ 最大震级", f"{filtered_df['震级'].max():.1f}")
col3.metric("📈 平均震级", f"{filtered_df['震级'].mean():.2f}")
col4.metric("📉 平均深度", f"{filtered_df['深度(km)'].mean():.1f} km")
col5.metric("📅 时间跨度", f"{(filtered_df['时间'].max() - filtered_df['时间'].min()).days} 天")

# ============================================================
# 图表展示
# ============================================================
st.header("📈 数据分析图表")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["震级分布", "时间分布", "深度分析", "原始数据", "🔬 关键发现"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_df['震级'], bins=30, kde=True, color='steelblue')
        ax.set_title('震级分布')
        ax.set_xlabel('震级')
        ax.set_ylabel('频次')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=filtered_df, x='深度(km)', y='震级', alpha=0.5, s=20)
        ax.set_title('震级 vs 深度')
        ax.set_xlabel('深度 (km)')
        ax.set_ylabel('震级')
        st.pyplot(fig)

with tab2:
    # 时间维度分析
    filtered_df['星期'] = filtered_df['时间'].dt.dayofweek
    filtered_df['小时'] = filtered_df['时间'].dt.hour
    weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
    filtered_df['星期名称'] = filtered_df['星期'].map(weekday_map)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        weekly_counts = filtered_df['星期名称'].value_counts().reindex(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
        sns.barplot(x=weekly_counts.index, y=weekly_counts.values, palette='viridis')
        ax.set_title('一周内各天地震分布')
        ax.set_xlabel('星期')
        ax.set_ylabel('地震次数')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        hourly_counts = filtered_df['小时'].value_counts().sort_index()
        sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette='coolwarm')
        ax.set_title('一天内各时段地震分布')
        ax.set_xlabel('小时')
        ax.set_ylabel('地震次数')
        st.pyplot(fig)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_df['深度(km)'], bins=30, kde=True, color='coral')
        ax.set_title('深度分布')
        ax.set_xlabel('深度 (km)')
        ax.set_ylabel('频次')
        st.pyplot(fig)
    with col2:
        # 深度区间统计
        depth_bins = [0, 10, 30, 70, 150, 300, 1000]
        depth_labels = ['0-10km', '10-30km', '30-70km', '70-150km', '150-300km', '300km+']
        filtered_df['深度区间'] = pd.cut(filtered_df['深度(km)'], bins=depth_bins, labels=depth_labels)
        depth_counts = filtered_df['深度区间'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=depth_counts.index, y=depth_counts.values, palette='rocket')
        ax.set_title('深度区间地震频次')
        ax.set_xlabel('深度区间')
        ax.set_ylabel('地震次数')
        st.pyplot(fig)

with tab4:
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button(
        label="📥 下载数据 (CSV)",
        data=filtered_df.to_csv(index=False).encode('utf-8-sig'),
        file_name='earthquake_filtered_data.csv',
        mime='text/csv'
    )

with tab5:
    st.markdown("""
    ## 🔬 关键发现：周六效应是“观测偏差”
    
    基于 **365天（29,801条）** 地震数据的分析验证。
    
    ---
    
    ### 📅 发现一：周六地震最多
    
    对全部地震数据的分析显示：
    
    | 排名 | 星期 | 地震次数 |
    |------|------|----------|
    | 🥇 最多 | 周六 | **635 次** |
    | 🥈 第二 | 周五 | 561 次 |
    | 🥉 第三 | 周三 | 552 次 |
    | 第四 | 周日 | 548 次 |
    | 第五 | 周一 | 539 次 |
    | 第六 | 周四 | 531 次 |
    | 第七 | 周二 | 524 次 |
    
    > 表面上看，**周六地震最多**，但这是真实的地球物理规律吗？
    
    ---
    
    ### 🧐 发现二：分层验证——周六效应只出现在小地震中
    
    为了验证“周六效应”是否真实存在，我将数据按震级分为两组：
    
    | 分组 | 震级范围 |
    |------|----------|
    | 🔹 小地震 | 2.5 级 ≤ 震级 < 4.5 级 |
    | 🔸 大地震 | 震级 ≥ 4.5 级 |
    
    #### 验证结果：
    
    | | 小地震 (< 4.5级) | 大地震 (≥ 4.5级) |
    |---|-----------------|------------------|
    | **地震最多的星期** | 🥇 **周六 (480次)** | 🥇 **周三 (166次)** |
    | **地震最少的星期** | 周二 (394次) | 周二 (130次) |
    
    > 💡 **关键结论**：如果“周六效应”是真实的地球物理规律，那么大地震也应该在周六最多。
    > 
    > 但事实是：**大地震最多的是周三，而不是周六**。
    > 
    > 这说明“周六效应”很可能不是地球的物理规律，而是 **“观测偏差”**。
    
    ---
    
    ### 💡 为什么会出现“周六效应”？
    
    周末人类活动减少，地震仪更容易捕捉到小地震。
    
    | 人类活动 | 工作日 | 周末 |
    |---------|--------|------|
    | 交通 | 🚗🚗🚗🚗🚗 | 🚗🚗 |
    | 工厂/采矿 | 🏭🏭🏭🏭🏭 | 🏭 |
    | 建筑施工 | 🚧🚧🚧🚧🚧 | 🚧 |
    | **背景噪声** | **高（掩盖小地震）** | **低（小地震被清晰记录）** |
    
    > 工作日人类活动产生的振动（文化噪声）会掩盖小地震的信号，导致记录到的数量偏少。
    > 周末噪声减少，小地震被更完整地记录下来，导致“周六地震多”的假象。
    
    ---
    
    ### 📈 可视化验证
    
    """)
    
    # 显示对比图表（如果你已经生成了 layer_comparison.png）
    try:
        st.image("../output/images/layer_comparison.png", caption="不同震级地震的一周分布对比")
    except:
        st.info("请运行 layer_analysis.py 生成对比图表")
    
    st.markdown("""
    ---
    
    ### 🎯 结论
    
    > **“周六效应”只存在于小地震中，是人為活动噪声造成的“观测偏差”，而非真实的地球物理规律。**
    
    | 验证维度 | 结论 |
    |---------|------|
    | 数据量 | 29,801 条（365天） |
    | 统计方法 | 震级分层验证 |
    | 核心发现 | 周六效应只出现在小地震中 |
    | 科学解释 | 周末人为噪声减少，观测更完整 |
    
    ---
    
    ### 📚 延伸思考
    
    这个发现与地震学中的 **“文化噪声”** 研究一致。科学家们甚至利用节假日期间的数据来研究微小地震活动。

    """)

# ============================================================
# 交互式地图
# ============================================================
st.header("🗺️ 地震位置地图")

# 限制显示数量避免地图卡顿（最多2000点）
map_df = filtered_df.head(2000) if len(filtered_df) > 2000 else filtered_df

if not map_df.empty:
    # 计算地图中心
    center_lat = map_df['纬度'].mean()
    center_lon = map_df['经度'].mean()

    # 创建地图
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2, tiles='CartoDB positron')

    # 添加地震标记
    for _, row in map_df.iterrows():
        mag = row['震级']
        if mag >= 6.0:
            color, radius = 'red', 12
        elif mag >= 5.0:
            color, radius = 'orange', 10
        elif mag >= 4.0:
            color, radius = 'yellow', 8
        else:
            color, radius = 'green', 6

        popup = f"""
        <b>地点:</b> {row['地点']}<br>
        <b>震级:</b> {row['震级']:.1f}<br>
        <b>深度:</b> {row['深度(km)']:.1f} km<br>
        <b>时间:</b> {row['时间']}
        """
        folium.CircleMarker(
            location=[row['纬度'], row['经度']],
            radius=radius,
            popup=folium.Popup(popup, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

    # 显示地图
    folium_static(m, width=1200, height=600)

else:
    st.info("当前筛选条件下没有数据可显示")

# ============================================================
# 页脚
# ============================================================
st.markdown("---")
st.caption("🌍 数据来源: USGS Earthquake Catalog | 地震数据统计器")