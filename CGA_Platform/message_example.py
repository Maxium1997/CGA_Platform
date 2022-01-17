from registration.models import User
from multi_relation.definitions import PaymentStatus
from cga_booking.models import RoomReservation
from cga_booking.definitions import ReservationUsages, ReservationStatus

message1 = ('Subject here',
            'Here is the message',
            'from@example.com',
            ['first@example.com', 'other@example.com'])


def reservation_pending_message(reservation: RoomReservation, recipient: User):
    subject = "訂單編號#" + reservation.serial_number + "｜Pending｜CGA Booking"

    reserved_room = reservation.content_object

    if recipient == reservation.created_by:
        mail_content = "Dear Customer, Greeting from CGA Platform\n\n" + \
                       "With reference to your reservation Serial Number " + reservation.serial_number + " as detailed below:\n\n" + \
                       "名稱Hotel：" + reserved_room.belongs2.name + "\n" + \
                       "地址Address：" + reserved_room.belongs2.address + "\n" + \
                       "房型Room：" + reserved_room.name + "\n" + \
                       "入住Check In：" + reservation.start_time.strftime("%Y/%m/%d") + "\n" + \
                       "退房Check Out：" + reservation.end_time.strftime("%Y/%m/%d") + "\n" + \
                       "用途Usage：" + list(ReservationUsages.__members__.values())[reservation.usage - 1].value[1] + "\n" + \
                       "訂單狀態Status：" + list(ReservationStatus.__members__.values())[reservation.status - 1].value[1] + "\n" + \
                       "付款狀態Payment Status：" + list(PaymentStatus.__members__.values())[reservation.payment_status - 1].value[
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
                       "With reference to your managed hotel " + reserved_room.belongs2 + " as detailed below:\n\n" + \
                       "預訂人Customer：" + reservation.created_by + "\n" + \
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

