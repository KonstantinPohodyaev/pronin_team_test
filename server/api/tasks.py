from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from server.payment.models import User, Collect, Payment


User = get_user_model()

COLLECT_SUBJECT = 'New Collect: {title}'
COLLECT_MESSAGE = 'You created new collect!'

PAYMENT_SUBJECT = 'New Payment Created!'
PAYMENT_MESSAGE = 'You created payment with amount = {amount}!. Thank you!'


@shared_task
def send_email_task(status: str, instance_pk: int, email: str) -> None:
    """Send email by entered status."""
    if status == 'collect':
        collect = Collect.objects.get(pk=instance_pk)
        subject = COLLECT_SUBJECT.format(title=collect.title)
        message = COLLECT_MESSAGE
    else:
        payment = Payment.objects.get(pk=instance_pk)
        subject = PAYMENT_SUBJECT
        message = PAYMENT_MESSAGE.format(amount=payment.amount)
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[email],
        from_email=None,
    )
