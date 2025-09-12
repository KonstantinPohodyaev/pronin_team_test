from django.core.mail import send_mail
from django.contrib.auth import get_user_model


User = get_user_model()

COLLECT_SUBJECT = 'New Collect: {title}'
COLLECT_MESSAGE = 'You created new collect!'

PAYMENT_SUBJECT = 'New Payment Created!'
PAYMENT_MESSAGE = 'You created payment with amount = {amount}!. Thank you!'


def send_email(status: str, instance, user) -> None:
    """Send email by entered status."""
    if status == 'collect':
        subject = COLLECT_SUBJECT.format(title=instance.title)
        message = COLLECT_MESSAGE
    else:
        subject = PAYMENT_SUBJECT
        message = PAYMENT_MESSAGE.format(amount=instance.amount)
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[user.email],
        from_email=None,
    )
