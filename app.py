import sys, os, tempfile
sys.path.append("src")
import streamlit as st
from decode import decode_qr
from features import url_features
from rules import rule_score

st.set_page_config(page_title="QR Code Threat Detector", page_icon="🔍")
st.title("🔍 Malicious QR Code Detector")
st.write("Upload a QR code image. The app decodes it and analyses the URL. It never opens the link.")

def analyse(url):
    f = url_features(url)
    score = rule_score(f)
    if f["is_shortener"]:
        verdict = "⚠️ UNVERIFIABLE: shortened link, destination hidden"
    elif score >= 3:
        verdict = "🚨 SUSPICIOUS"
    else:
        verdict = "✅ Likely safe"
    return f, score, verdict

tab1, tab2 = st.tabs(["Upload QR image", "Paste a URL"])

with tab1:
    file = st.file_uploader("QR image", type=["png", "jpg", "jpeg"])
    if file:
        st.image(file, width=250)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(file.read())
            path = tmp.name
        r = decode_qr(path)
        os.remove(path)
        if not r["decoded"]:
            st.error("No QR code could be decoded.")
        else:
            st.code(r["decoded"])
            f, score, verdict = analyse(r["decoded"])
            st.subheader(verdict)
            st.metric("Risk score", score)
            st.json(f)

with tab2:
    url = st.text_input("URL to analyse (text only, never opened)")
    if url:
        f, score, verdict = analyse(url)
        st.subheader(verdict)
        st.metric("Risk score", score)
        st.json(f)