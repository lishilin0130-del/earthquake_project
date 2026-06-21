# 🌍 地震数据统计器

基于 Python 和 USGS API 的地震数据获取、分析和可视化工具。

## 📊 项目简介

本项目从美国地质调查局（USGS）获取实时地震数据，进行统计分析，并生成交互式可视化地图，帮助直观了解全球地震分布规律。

## 🎯 功能列表

- ✅ **数据获取**：从 USGS API 获取最近30天的真实地震数据
- ✅ **数据清洗**：自动过滤无效数据，整理为标准格式
- ✅ **统计分析**：计算震级、深度等关键指标的统计信息
- ✅ **可视化图表**：生成震级分布、深度分布、关系散点图等
- ✅ **交互地图**：在地图上标记地震位置，点击查看详情

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10 | 编程语言 |
| Pandas | 数据处理 |
| Matplotlib + Seaborn | 数据可视化 |
| Folium | 交互式地图 |
| Requests | API 数据获取 |
| Git + GitHub | 版本控制 |

## 📁 项目结构

```text
EARTHQUAKE_PROJECT/
├── data/                    # 原始数据
│   └── earthquakes_raw.csv
├── scripts/                 # Python 脚本
│   ├── get_data.py          # 数据获取
│   ├── analyze_data.py      # 数据分析与可视化
│   └── query_earthquakes.py # 地震查询与地图
├── output/                  # 输出结果
│   └── images/              # 统计图表
├── tools/                   # 工具脚本
├── requirements.txt         # 依赖列表
└── README.md                # 项目说明
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/lishilin0130-del/earthquake_project.git
cd earthquake_project
```

### 2. 创建虚拟环境

```bash
conda create -n earthquake python=3.10
conda activate earthquake
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 获取数据

```bash
cd scripts
python get_data.py
```

### 5. 生成图表

```bash
python analyze_data.py
```

### 6. 查询地震并生成地图

```bash
python query_earthquakes.py
```

## 📊 效果展示

### 震级分布图

![震级分布](output/images/magnitude_distribution.png)

### 地震位置地图

交互式地图上，不同颜色的圆点代表不同震级的地震：

- 🔴 红色：≥ 6.0 级
- 🟠 橙色：5.0 - 5.9 级
- 🟡 黄色：4.0 - 4.9 级
- 🟢 绿色：2.5 - 3.9 级

## 📈 数据来源

数据来源于 [USGS 地震目录 API](https://earthquake.usgs.gov/fdsnws/event/1/query)

## 👤 作者

- **Shilin Li** (lishilin0130-del)
- 完成时间：2026年6月

## 📝 许可证

MIT License
```

---

## ✅ 操作步骤

1. 复制上面的全部内容
2. 打开 VS Code 中的 `README.md` 文件
3. `Ctrl + A` 全选，`Ctrl + V` 粘贴
4. `Ctrl + S` 保存
5. 在终端执行：

```bash
git add README.md
git commit -m "修复 README 格式"
git push
```

---

刷新 GitHub 页面，应该能看到格式正常的 README 了！🚀