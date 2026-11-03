import cv2

try:
    from pyzbar.pyzbar import decode as zbar_decode
    HAS_ZBAR = True
except Exception:
    HAS_ZBAR = False

_detector = cv2.QRCodeDetector()

def decode_qr(path):
    img = cv2.imread(path)
    if img is None:
        return {"decoded": None, "n_codes": 0, "qr_w": 0, "qr_h": 0, "decoder": "failed"}

    if HAS_ZBAR:
        results = zbar_decode(img)
        if results:
            r = results[0]
            return {"decoded": r.data.decode("utf-8", errors="ignore"),
                    "n_codes": len(results),
                    "qr_w": r.rect.width, "qr_h": r.rect.height,
                    "decoder": "pyzbar"}

    data, pts, _ = _detector.detectAndDecode(img)
    if data:
        if pts is not None:
            w = int(pts[0][:, 0].max() - pts[0][:, 0].min())
            h = int(pts[0][:, 1].max() - pts[0][:, 1].min())
        else:
            w, h = img.shape[1], img.shape[0]
        return {"decoded": data, "n_codes": 1, "qr_w": w, "qr_h": h, "decoder": "opencv"}

    return {"decoded": None, "n_codes": 0, "qr_w": 0, "qr_h": 0, "decoder": "failed"}