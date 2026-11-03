import random, string, pandas as pd

random.seed(42)
SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"]

def short_link():
    code = "".join(random.choices(string.ascii_letters + string.digits, k=7))
    return f"https://{random.choice(SHORTENERS)}/{code}"

mal = [u.strip() for u in open("data/raw_malicious.txt") if u.strip()][:1000]
ben = ["https://" + d.strip() for d in open("data/raw_benign.txt") if d.strip()][:1000]

rows = [(u, 1) for u in mal] + [(u, 0) for u in ben]
random.shuffle(rows)

out = []
for url, label in rows:
    shortened = random.random() < 0.20
    out.append({"original_url": url,
                "payload": short_link() if shortened else url,
                "label": label,
                "is_shortened_sim": int(shortened)})

pd.DataFrame(out).to_csv("data/dataset.csv", index=False)
print("Saved", len(out), "rows")