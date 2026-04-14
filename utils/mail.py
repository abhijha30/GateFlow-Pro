import smtplib
from email.message import EmailMessage

def send_qr(to_email, file_path):

    EMAIL = "abhitheboss2004@gmail.com"
    PASSWORD = "vdso vsez dgzm jkgd"  # must be APP PASSWORD

    try:
        msg = EmailMessage()
        msg["Subject"] = "🎟️ Your Event Pass"
        msg["From"] = EMAIL
        msg["To"] = to_email

        msg.set_content("Your registration is approved. QR pass attached.")

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="image",
                subtype="png",
                filename="qr.png"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print("✅ MAIL SENT")

    except Exception as e:
        print("❌ MAIL ERROR:", e)
