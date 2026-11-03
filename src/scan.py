import sys
from decode import decode_qr
from features import url_features
from rules import rule_score

r = decode_qr(sys.argv[1])
if not r["decoded"]:
    print("No QR code found"); sys.exit()
f = url_features(r["decoded"])
print("URL:", r["decoded"])
print("Risk score:", rule_score(f), "| Shortener:", bool(f["is_shortener"]))
print("Verdict:", "SUSPICIOUS" if rule_score(f) >= 3 or f["is_shortener"] else "Likely safe")