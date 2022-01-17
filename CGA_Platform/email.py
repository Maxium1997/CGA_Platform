import random
import base64

from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError, SMTPException

from CGA_Platform.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from registration.models import User
from cga_booking.models import Room, RoomReservation
from cga_booking.definitions import ReservationStatus, ReservationUsages
from multi_relation.definitions import PaymentStatus


def sent_confirmation_email_to(user: User):
    # strSmtp = "smtp.gmail.com:587"
    # 主機
    account_str = "cgaplatform@gmail.com"      # 備援信箱：
    password_str = "CGAplateform86925"

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
                   "https://cgaplatform.pythonanywhere.com/accounts/confirm_email/{}\n\n".format(str_base64_bytes_encoded_username) + \
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


def sent_reservation_info(customer: User, reservation: RoomReservation):
    # strSmtp = "smtp.gmail.com:587"
    # 主機
    account_str = "cgaplatform@gmail.com"      # 備援信箱：
    password_str = "CGAplateform86925"
    reserved_room = Room.objects.get(id=reservation.object_id)

    # encode the verified email
    email = customer.email
    email_bytes = email.encode('ascii')
    base64_bytes = base64.b64encode(email_bytes)
    base64_email = base64_bytes.decode('ascii')

    mail_content = ""
    subject_content = ""
    if reservation.status == ReservationStatus.Pending.value[0]:
        subject_content = "訂單編號：" + reservation.serial_number + "｜審查中｜眷探處所｜CGA Platform"
        mail_content = "Dear Customer, Greeting from CGA Info System!!!!!!\n\n" + \
                       "With reference to your reservation Serial Number " + reservation.serial_number + "as detailed below:\n\n" + \
                       "Hotel：" + reserved_room.belongs2.name + "\n" + \
                       "Address" + reserved_room.belongs2.address + "\n" + \
                       "Room：" + reserved_room.name + "\n" + \
                       "Check In：" + reservation.start_time.strftime("%Y年 %m月 %d日") + "\n" + \
                       "Check Out：" + reservation.end_time.strftime("%Y年 %m月 %d日") + "\n" + \
                       "Usage：" + list(ReservationUsages.__members__.values())[reservation.usage-1].value[1] + "\n" + \
                       "Status：" + list(ReservationStatus.__members__.values())[reservation.status-1].value[1] + "\n" + \
                       "Payment Status：" + list(PaymentStatus.__members__.values())[reservation.payment_status-1].value[1] + "\n\n" + \
                       "You can press here to check your reservation detail, " +\
                       "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/info\n\n" + \
                       "or you can press here to cancel your reservation, " + \
                       "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/cancel\n\n" +  \
                       "I hope we can meet in time. If you have any problem, please contact us with the mail " + \
                       reserved_room.belongs2.contact_email + " " \
                       "or you can call the phone " + reserved_room.belongs2.contact_phone + "\n\n" + \
                       "Hope you have a nice trip.\n\n" + "Regards, CGA Platform Developer."

    elif reservation.status == ReservationStatus.Passed.value[0]:
        subject_content = "訂單編號：" + reservation.serial_number + "｜審查已通過｜眷探處所｜CGA Platform"
        mail_content = "Dear Customer, \n" + \
                       "Congratulation! Your reservation had been passed. " + \
                       "When you check in, please show the link to the hotel staff, " \
                       "they will help you to check the reservation.\n\n" + \
                       "Reservation Detail Link, press here, " + \
                       "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/info" + "\n\n" + \
                       "Check In Link, press here, " + \
                       "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/check_in" + "\n\n" + \
                       "We hope to meet you that day.\n\n" + "Regards, CGA Info System Developer."

    elif reservation.status == ReservationStatus.Canceled.value[0]:
        subject_content = "訂單編號：" + reservation.serial_number + "｜已取消｜眷探處所｜CGA Platform"
        mail_content = "Dear Customer, \n" + \
                       "Sorry, Your reservation had been canceled. " + \
                       "If you have any problem, you can contact us through this mail, cga.info.system@gmail.com\n\n" + \
                       "Reservation Detail Link, press here, " + \
                       "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/info" + "\n\n" + \
                       "Hope to see you next time.\n\n" + "Regards, CGA Info System Developer."
    else:
        pass

    msg = MIMEText(mail_content)
    msg["Subject"] = subject_content
    # 郵件標題
    mail_to = customer.email

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


def sent_reservation_mail(reservation: RoomReservation, recipient: User):
    subject = "訂單編號#" + reservation.serial_number + "｜{}｜CGA Booking"
    mail_content = ''
    reserved_room = reservation.content_object

    if reservation.status == ReservationStatus.Pending.value[0]:
        subject = "訂單編號#" + reservation.serial_number + "｜Pending｜CGA Booking"

        if recipient == reservation.created_by:
            mail_content = "Dear Customer, Greeting from CGA Platform\n\n" + \
                           "With reference to your reservation Serial Number " + reservation.serial_number + " as detailed below:\n\n" + \
                           "名稱Hotel：" + reserved_room.belongs2.name + "\n" + \
                           "地址Address：" + reserved_room.belongs2.address + "\n" + \
                           "房型Room：" + reserved_room.name + "\n" + \
                           "入住Check In：" + reservation.start_time.strftime("%Y/%m/%d") + "\n" + \
                           "退房Check Out：" + reservation.end_time.strftime("%Y/%m/%d") + "\n" + \
                           "用途Usage：" + list(ReservationUsages.__members__.values())[reservation.usage - 1].value[
                               1] + "\n" + \
                           "訂單狀態Status：" + list(ReservationStatus.__members__.values())[reservation.status - 1].value[
                               1] + "\n" + \
                           "付款狀態Payment Status：" + \
                           list(PaymentStatus.__members__.values())[reservation.payment_status - 1].value[
                               1] + "\n\n" + \
                           "You can press the following link to check your reservation detail, " + \
                           "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/info\n\n" + \
                           "or you can press here to cancel your reservation, " + \
                           "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/cancel\n\n" + \
                           "Hope we can meet in time. If you have any problem, please contact us with the mail " + \
                           reserved_room.belongs2.contact_email + "\n" + \
                           "or you can call the phone " + reserved_room.belongs2.contact_phone + "\n\n" + \
                           "Hope you have a nice trip.\n\n" + "Regards, CGA Platform Developer. dW."

        elif recipient == reserved_room.belongs2.manager:
            mail_content = "Dear Manager, Greeting from CGA Platform\n\n" + \
                           "With reference to your managed hotel " + reserved_room.belongs2.name + " as detailed below:\n\n" + \
                           "名稱Hotel：" + reserved_room.belongs2.name + "\n" + \
                           "地址Address：" + reserved_room.belongs2.address + "\n" + \
                           "房型Room：" + reserved_room.name + "\n" + \
                           "入住Check In：" + reservation.start_time.strftime("%Y/%m/%d") + "\n" + \
                           "退房Check Out：" + reservation.end_time.strftime("%Y/%m/%d") + "\n" + \
                           "用途Usage：" + list(ReservationUsages.__members__.values())[reservation.usage - 1].value[
                               1] + "\n" + \
                           "訂單狀態Status：" + list(ReservationStatus.__members__.values())[reservation.status - 1].value[
                               1] + "\n" + \
                           "付款狀態Payment Status：" + \
                           list(PaymentStatus.__members__.values())[reservation.payment_status - 1].value[
                               1] + "\n\n" + \
                           "Please press the following link to check the reservation detail, " + \
                           "https://cgaplatform.pythonanywhere.com/reservation/" + reservation.serial_number + "/info\n\n" + \
                           "Regards, CGA Platform Developer. dW."
    elif reservation.status == ReservationStatus.Passed.value[0]:
        subject = "訂單編號#" + reservation.serial_number + "｜Passed｜CGA Booking"
    elif reservation.status == ReservationStatus.Canceled.value[0]:
        subject = "訂單編號#" + reservation.serial_number + "｜Canceled｜CGA Booking"
    else:
        pass

    msg = MIMEText(mail_content)
    msg["Subject"] = subject    # 郵件標題
    mail_to = recipient.email

    server = SMTP("smtp.gmail.com:587")     # 建立連線
    # server = SMTP(strSmtp)
    server.ehlo()   # 跟主機溝通
    server.starttls()   # TTLS安全驗證

    try:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, mail_to, msg.as_string())
        hint = "郵件已發送"
    except SMTPAuthenticationError:
        hint = "無法登入"
    except:
        hint = "郵件發送產生錯誤"
    server.quit()   # 關閉連線
