import pandas as pd, matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix,
                             ConfusionMatrixDisplay)
from decode import decode_qr
from features import url_features
from rules import rule_predict

df = pd.read_csv("data/dataset.csv")

dec = df["image"].apply(decode_qr).apply(pd.Series)
df = pd.concat([df, dec], axis=1)
print("Decode success rate:", df["decoded"].notna().mean())
df = df[df["decoded"].notna()].reset_index(drop=True)

feats = pd.DataFrame([url_features(u) for u in df["decoded"]])
feats["qr_payload_len"] = df["decoded"].str.len()
feats["qr_w"], feats["n_codes"] = df["qr_w"], df["n_codes"]
y = df["label"]

X_tr, X_te, y_tr, y_te, idx_tr, idx_te = train_test_split(
    feats, y, df.index, test_size=0.3, stratify=y, random_state=42)

rule_pred = X_te.apply(rule_predict, axis=1)

rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_tr, y_tr)
lr = LogisticRegression(max_iter=2000).fit(X_tr, y_tr)
preds = {"Rule-based": rule_pred, "LogReg": lr.predict(X_te), "RandomForest": rf.predict(X_te)}

short_mask = df.loc[idx_te, "is_shortened_sim"].values == 1

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, (name, p) in zip(axes, preds.items()):
    p = pd.Series(p).values
    print(f"\n=== {name} (all test data) ===")
    print(classification_report(y_te, p, target_names=["benign", "malicious"]))
    tn, fp, fn, tp = confusion_matrix(y_te, p).ravel()
    print(f"FP={fp}  FN={fn}  (FP rate={fp/(fp+tn):.2%}, FN rate={fn/(fn+tp):.2%})")

    print(f"--- {name}: SHORTENED URLs only ---")
    print(classification_report(y_te[short_mask], p[short_mask], zero_division=0,
                                target_names=["benign", "malicious"]))
    print(f"--- {name}: NON-SHORTENED only ---")
    print(classification_report(y_te[~short_mask], p[~short_mask], zero_division=0,
                                target_names=["benign", "malicious"]))
    ConfusionMatrixDisplay.from_predictions(y_te, p, ax=ax, colorbar=False)
    ax.set_title(name)
plt.tight_layout(); plt.savefig("results/confusion_matrices.png", dpi=150)

imp = pd.Series(rf.feature_importances_, index=feats.columns).sort_values()
imp.plot.barh(figsize=(7, 6), title="RandomForest feature importance")
plt.tight_layout(); plt.savefig("results/feature_importance.png", dpi=150)
print("\nSaved charts to results/")

flag = (X_te["is_shortener"] == 1).values
combo = (pd.Series(rule_pred).values | flag).astype(int)
print("\n=== Rule + shortener flag ===")
print(classification_report(y_te, combo, target_names=["benign", "malicious"]))
tn, fp, fn, tp = confusion_matrix(y_te, combo).ravel()
print(f"FP={fp}  FN={fn}  (FP rate={fp/(fp+tn):.2%}, FN rate={fn/(fn+tp):.2%})")

print("--- Rule + shortener flag: SHORTENED URLs only ---")
print(classification_report(y_te[short_mask], combo[short_mask], zero_division=0,
                            target_names=["benign", "malicious"]))