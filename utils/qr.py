import qrcode

def generate_qr(data):
    file_path = f"{data}.png"
    img = qrcode.make(data)
    img.save(file_path)
    return file_path
