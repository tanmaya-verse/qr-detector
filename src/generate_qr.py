import pandas as pd, qrcode

df = pd.read_csv("data/dataset.csv")
for i, row in df.iterrows():
    qrcode.make(row["payload"]).save(f"data/qr/{i}.png")
df["image"] = [f"data/qr/{i}.png" for i in range(len(df))]
df.to_csv("data/dataset.csv", index=False)
print("Generated", len(df), "QR images")