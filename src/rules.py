def rule_score(f):
    s = 0
    s += 3 * f["has_ip"]
    s += 2 * f["has_at"]
    s += 2 * f["punycode"]
    s += 2 * f["risky_tld"]
    s += 1 * (f["n_subdomains"] >= 3)
    s += 1 * (f["url_len"] > 75)
    s += 1 * (f["n_hyphens"] >= 2)
    s += min(f["n_keywords"], 3)
    s += 1 * (1 - f["is_https"])
    s += 1 * f["non_standard_port"]
    return s

def rule_predict(f, threshold=3):
    return int(rule_score(f) >= threshold)