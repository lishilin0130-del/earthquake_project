# earthquake_project

基础地震项目骨架（Python + PyTorch）。包含数据拉取、预处理、训练与本地预测服务示例。

Quick start

1. 创建虚拟环境并安装依赖：

```bash
python -m venv .venv
.
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

2. 下载示例数据并运行 ETL：

```bash
python -m src.data.etl --url "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv" --out data/raw.csv
```

3. 训练示例模型：

```bash
python -m src.train --data_path data/raw.csv --model_out models/model.pth
```

4. 启动预测服务：

```bash
uvicorn src.api.predict:app --reload --port 8000
```
