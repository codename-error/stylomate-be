import smtplib
from email.message import EmailMessage

def send_verification_email(sender_email, receiver_email, verification_code):
    # Buat email
    email = EmailMessage()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = "kode verifikasi Email Kamu"

    # Konten HTML email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        .button {{
        background-color: #007bff;
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
        }}
    </style>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
    <img src="https://prakerja.go.id/images/logo-prakerja.png" alt="STYLO MATE" width="120">
    <h2>Verifikasi Email Kamu</h2>
    <p>hanya beberapa langkah lagi sebelum kamu dapat menggunakan akun stylo mate.</p>
    <p>Berikut adalah code email verivication:</p>
    <h1 style="font-size: 24px; color: #007bff;">{verification_code}</h1>
    <p>Jika kamu tidak melakukan ini, akun kamu tidak akan aktif.</p>
    <p><small>Kode verifikasi ini akan berakhir dalam waktu 24 jam.<br>
    Bila link tidak berfungsi atau sudah berakhir masa berlakunya, silakan lakukan pendaftaran ulang.</small></p>
    <br><br>
    <footer style="font-size: 12px; color: gray;">
        <p>Stylo mate</p>
        </p>
    </footer>
    </body>
    </html>
    """

        # Tambahkan konten HTML ke email
    email.set_content("Gunakan email client yang mendukung HTML untuk melihat isi pesan.")
    email.add_alternative(html_content, subtype='html')

    # Kirim email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, "ggcc rhjm sylr sjsi")  # Ganti dengan App Password Gmail kamu
        server.send_message(email)
        print("Email sent successfully!")