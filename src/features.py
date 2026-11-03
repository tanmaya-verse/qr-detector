import math, re
from urllib.parse import urlparse
import tldextract

SHORTENERS = {"bit.ly","tinyurl.com","t.co","goo.gl","is.gd","cutt.ly","ow.ly","rebrand.ly"}
KEYWORDS = ["login","verify","secure","account","update","bank","paypal","signin","confirm","password","wallet","free","bonus"]
RISKY_TLDS = {"xyz","top","tk","ml","ga","cf","gq","click","work","support","zip"}

def entropy(s):
    if not s: return 0
    p = [s.count(c)/len(s) for c in set(s)]
    return -sum(x*math.log2(x) for x in p)

def url_features(url):
    u = url if "://" in url else "http://" + url
    p = urlparse(u)
    ext = tldextract.extract(u)
    host = p.netloc.lower()
    domain = ".".join([ext.domain, ext.suffix]).strip(".")
    try:
        port = p.port
    except ValueError:
        port = None
    return {
        "url_len": len(url),
        "host_len": len(host),
        "path_len": len(p.path),
        "n_dots": host.count("."),
        "n_subdomains": len([s for s in ext.subdomain.split(".") if s]),
        "n_hyphens": host.count("-"),
        "n_digits": sum(c.isdigit() for c in url),
        "has_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}(:\d+)?", host))),
        "has_at": int("@" in url),
        "is_https": int(p.scheme == "https"),
        "n_params": len(p.query.split("&")) if p.query else 0,
        "n_keywords": sum(k in url.lower() for k in KEYWORDS),
        "risky_tld": int(ext.suffix.split(".")[-1] in RISKY_TLDS),
        "punycode": int("xn--" in host),
        "entropy": entropy(url),
        "is_shortener": int(domain in SHORTENERS),
        "non_standard_port": int(bool(port) and port not in (80, 443)),
    }