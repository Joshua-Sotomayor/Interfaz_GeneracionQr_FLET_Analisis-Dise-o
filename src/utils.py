# src/utils.py
import qrcode
import json
import base64
from io import BytesIO

def generate_qr_image(data):
    """Genera imagen QR en formato base64"""
    qr_data = json.dumps({
        "producto": data["productType"],
        "cantidad": data["quantity"],
        "proveedor": data["supplier"],
        "fecha": data["date"]
    }, ensure_ascii=False)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64