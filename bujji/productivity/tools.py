"""
Productivity Tools — QR Code, Password Generator & Utilities
============================================================
Generates QR codes, creates secure passwords, and performs mathematical calculations.
"""

import random
import string
try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


def generate_qr_code(text_or_url, filename="qrcode.png"):
    """Generate a QR code image file from text or URL."""
    if not QR_AVAILABLE:
        print("[WARNING] qrcode module is not installed. Run `pip install qrcode[pil]`")
        return None

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(text_or_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filepath = OUTPUT_DIR / filename
        img.save(filepath)
        return str(filepath)
    except Exception as e:
        print(f"[QR Code Error] {e}")
        return None


def generate_password(length=16, include_symbols=True):
    """Generate a strong, random password."""
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    password = "".join(random.choice(chars) for _ in range(length))
    return password


def calculate_expression(expression):
    """Safely evaluate mathematical expressions."""
    try:
        ex = expression.lower()
        ex = ex.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divide", "/").replace("x", "*")
        allowed = "0123456789+-*/(). "
        if all(c in allowed for c in ex):
            res = eval(ex)
            return str(res)
        return "Invalid characters in mathematical expression."
    except Exception as e:
        return f"Calculation Error: {e}"
