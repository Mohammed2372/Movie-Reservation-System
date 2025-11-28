from django.core.mail import send_mail
from django.conf import settings


def send_ticket_email(booking):
    subject = f"Your Ticket for {booking.showtime.movie.title}"

    seats = booking.tickets.all()
    seat_list = ", ".join([f"{t.seat.row}{t.seat.number}" for t in seats])

    message = f"""
    Hello {booking.user.username},
    
    Your booking is confirmed!
    
    Movie:  {booking.showtime.movie.title}
    Cinema: {booking.showtime.screen.theater.name}
    Screen: {booking.showtime.screen.name}
    Time:   {booking.showtime.start_time.strftime("%Y-%m-%d %H:%M")}
    
    Seats:  {seat_list}
    
    Total Paid: ${booking.tickets.first().price * seats.count()}
    
    Please show this email at the entrance.
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.user.email],
            fail_silently=False,
        )
        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
