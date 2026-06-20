"""最小可运行的 PyTorch 训练示例（演示用）"""
import argparse
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader


class SimpleModel(nn.Module):
    def __init__(self, in_dim: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(in_dim, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, x):
        return self.net(x)


def load_data(path: str):
    df = pd.read_csv(path)
    # 简化：用数值列的前 N 列作为特征，目标用深度(如果存在)或次序
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(num_cols) < 2:
        raise ValueError("数据中没有足够的数值列用于训练")
    X = df[num_cols[:-1]].fillna(0).values.astype("float32")
    y = df[num_cols[-1]].fillna(0).values.astype("float32")
    return X, y


def train(args):
    X, y = load_data(args.data_path)
    Xtr, Xv, ytr, yv = train_test_split(X, y, test_size=0.2)
    train_loader = DataLoader(TensorDataset(torch.from_numpy(Xtr), torch.from_numpy(ytr)), batch_size=32, shuffle=True)
    model = SimpleModel(in_dim=X.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()
    for epoch in range(args.epochs):
        model.train()
        total = 0
        for xb, yb in train_loader:
            pred = model(xb)
            loss = loss_fn(pred.squeeze(), yb)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += loss.item()
        print(f"Epoch {epoch+1}/{args.epochs}, loss={total:.4f}")
    torch.save(model.state_dict(), args.model_out)
    print(f"Saved model to {args.model_out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", required=True)
    parser.add_argument("--model_out", required=True)
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()
    train(args)


if __name__ == "__main__":
    main()
