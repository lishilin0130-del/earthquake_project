"""简单 ETL：从 USGS CSV 拉取并保存为本地 CSV"""
import argparse
import requests
import pandas as pd


def fetch_usgs_csv(url: str, out_path: str):
    resp = requests.get(url)
    resp.raise_for_status()
    df = pd.read_csv(pd.compat.StringIO(resp.text))
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    fetch_usgs_csv(args.url, args.out)


if __name__ == "__main__":
    main()
