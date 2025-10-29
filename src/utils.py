import qrcode
import base64
from io import BytesIO

def generate_qr_image(url_data):
    """Genera imagen QR en formato base64 a partir de una URL"""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    # ⭐️ CAMBIO: Añadimos la URL como dato
    qr.add_data(url_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64