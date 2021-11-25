import random
import base64

from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError, SMTPException

from registration.models import User


def sent_confirmation_email_to(user: User):
    # strSmtp = "smtp.gmail.com:587"
    # 主機
    account_str = "cgaplatform@gmail.com"      # 備援信箱：
    password_str = "CGAplatform86925"

    # encode the verified email
    email = user.email
    email_bytes = email.encode('utf-8')
    base64_bytes = base64.b64encode(email_bytes)
    base64_email = base64_bytes.decode('utf-8')

    # encode username
    username = str(user.username)
    encoded_username = username.encode('utf-8')
    base64_bytes_encoded_username = base64.b64encode(encoded_username)
    str_base64_bytes_encoded_username = base64_bytes_encoded_username.decode('utf-8')

    subject_content = "CGA Platform/Confirm your email address"
    mail_content = "Hi Dear {},\n\n".format(user.username) + \
                   "Thanks for signing up for CGA Platform!\n\n" + \
                   "Please press the following link below to confirm your email address." + \
                   "This means you will be able to have a full experience in our website, " + \
                   "or if you forget your password, it can help you to reset it.\n\n" + \
                   "http://cgaplatform.pythonanywhere.com/accounts/confirm_email/{}\n\n".format(str_base64_bytes_encoded_username) + \
                   "Note: If you can't click the link from your email program, " \
                   "you also can copy the URL and paste it into your web browser.\n\n" + \
                   "If you don't want to use CGA Platform, just ignore this message.\n\n" + \
                   "Hope you can have a wonderful experience in CGA Platform.\n\n" + \
                   "The CGA Platform developer."

    msg = MIMEText(mail_content)
    msg["Subject"] = subject_content
    # 郵件標題
    mail_to = email

    server = SMTP("smtp.gmail.com:587")
    # server = SMTP(strSmtp)
    # 建立連線
    server.ehlo()
    # 跟主機溝通
    server.starttls()
    # TTLS安全驗證

    try:
        server.login(account_str, password_str)
        server.sendmail(account_str, mail_to, msg.as_string())
        hint = "郵件已發送"
    except SMTPAuthenticationError:
        hint = "無法登入"
    except:
        hint = "郵件發送產生錯誤"
    server.quit()
    # 關閉連線
