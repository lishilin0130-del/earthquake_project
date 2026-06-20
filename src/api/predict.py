from fastapi import FastAPI
from pydantic import BaseModel
import torch
import torch.nn as nn

app = FastAPI()


class InputData(BaseModel):
    features: list[float]


class SimpleModel(nn.Module):
    def __init__(self, in_dim: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(in_dim, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, x):
        return self.net(x)


model: SimpleModel | None = None


@app.on_event("startup")
def load_model():
    global model
    # 如果没有模型文件，则创建一个随机模型（供示例）
    try:
        dummy_in = 3
        model = SimpleModel(dummy_in)
        model.load_state_dict(torch.load("models/model.pth", map_location="cpu"))
        model.eval()
        print("Loaded model from models/model.pth")
    except Exception:
        print("No trained model found; API will use untrained example model")


@app.post("/predict")
def predict(data: InputData):
    global model
    import numpy as np
    x = torch.tensor([data.features], dtype=torch.float32)
    if model is None:
        m = SimpleModel(x.shape[1])
    else:
        m = model
    with torch.no_grad():
        out = m(x).numpy().tolist()
    return {"prediction": out}
