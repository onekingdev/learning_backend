from django.core.mail import send_mail
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import graphene


# Send mail with django-mailer
class SendMail(graphene.Mutation):
    email = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        send_mail(
            'Subject',
            'Message.',
            settings.SENDGRID_DEFAULT_SENDER,
            [email],
            fail_silently=False,
        )

        return SendMail(email=email)


class SendMailSendgrid(graphene.Mutation):
    email = graphene.String()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        message = Mail(
            from_email=settings.SENDGRID_DEFAULT_SENDER,
            to_emails=[email],
            subject='Subject',
            plain_text_content='Message.',
        )
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            return str(e)

        return SendMailSendgrid(email=email, message=message)


class Mutation(graphene.ObjectType):
    send_mail = SendMail.Field()
    send_mail_sendgrid = SendMailSendgrid.Field()
