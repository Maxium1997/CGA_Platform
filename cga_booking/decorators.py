from datetime import datetime


def reservation_time_validate(reserved_room, check_in_time: datetime.date, check_out_time: datetime.date):
    cit = datetime.combine(check_in_time, datetime.strptime('1500', "%H%M").time())
    cot = datetime.combine(check_out_time, datetime.strptime('1200', "%H%M").time())
    for reservation in reserved_room.reservations.all():
        rcit = reservation.start_time
        rcot = reservation.end_time
        if rcit <= cit <= rcot or rcit <= cot <= rcot or cit <= rcit <= rcot <= cot or rcit <= cit <= cot <= rcot:
            return False
    return True
