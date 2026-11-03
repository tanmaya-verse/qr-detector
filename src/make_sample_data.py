import random

random.seed(1)
brands = ["paypal", "amazon", "netflix", "microsoft", "apple", "sbi", "hdfc", "icici", "google", "facebook"]
words = ["login", "verify", "secure", "account", "update", "signin", "confirm", "wallet", "bonus", "free"]
tlds = ["xyz", "top", "tk", "ml", "ga", "cf", "click", "work", "support", "com", "net", "info"]

def rnd(n=6):
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=n))

def malicious():
    b, w, t = random.choice(brands), random.choice(words), random.choice(tlds)
    kind = random.randint(1, 4)
    if kind == 1:
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        return f"http://{ip}/{w}/{b}.php?id={rnd(8)}"
    if kind == 2:
        return f"http://{b}-{w}.{t}/{w}?session={rnd(16)}"
    if kind == 3:
        return f"https://{w}.{b}.{random.choice(words)}-{rnd(4)}.{t}/index.html"
    return f"http://{b}.com@{rnd(8)}.{t}/{w}"

benign_domains = ["google.com", "wikipedia.org", "github.com", "python.org", "stackoverflow.com",
                  "bbc.com", "nytimes.com", "amazon.com", "microsoft.com", "apple.com",
                  "linkedin.com", "reddit.com", "mozilla.org", "nasa.gov", "who.int",
                  "harvard.edu", "mit.edu", "ox.ac.uk", "iitb.ac.in", "gov.in",
                  "flipkart.com", "zomato.com", "swiggy.com", "hotstar.com", "irctc.co.in"]
paths = ["", "/", "/about", "/contact", "/search?q=python", "/docs/index.html", "/news/today"]

with open("data/raw_malicious.txt", "w") as f:
    f.write("\n".join(malicious() for _ in range(500)))
with open("data/raw_benign.txt", "w") as f:
    f.write("\n".join(random.choice(benign_domains) + random.choice(paths) for _ in range(500)))
print("Sample data created")