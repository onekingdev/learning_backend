from students.models import Student
from block.models import BlockQuestionPresentation

from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count
from datetime import timedelta
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from games.models import PlayGameTransaction
from payments.models import PaymentHistory
from users.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from app.settings.env import IS_PRODUCTION, DOMAIN_WITHOU_PRTC
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
def sendReportMail():
    print("===========starting sendReportMail/"+timezone.now()+"=============" )
    email_title = "Report"
    email_template_name = "emails/report/index.html"
    email_receivers = ["armin@learnwithsocrates.com"]
    project_name = "Prod Server" if settings.IS_PRODUCTION else "Dev Server"

    today = timezone.now()
    yesterday = today - timedelta(days=1)
    userHistory = (User.objects
        .filter((Q(create_timestamp__gt = yesterday) & Q(create_timestamp__lte = today)) | (Q(last_login__gt = yesterday) & Q(last_login__lte = today)))
        .annotate(num_correct_questions=Count('student__studentblockquestionpresentationhistory__block_question_presentation__id', filter=Q(student__studentblockquestionpresentationhistory__block_question_presentation__chosen_answer=True)))
        .annotate(num_wrong_questions=Count('student__studentblockquestionpresentationhistory__block_question_presentation__id', filter=Q(student__studentblockquestionpresentationhistory__block_question_presentation__chosen_answer=False)))
        .annotate(num_purchased_collectibles=Count('student__studentcollectible__id', filter=Q(student__studentcollectible__update_timestamp__gt=yesterday) & Q(student__studentcollectible__update_timestamp__lte=today)))
        .all()
    )
    for user in userHistory:
        try:
            coin_wallet = user.student.coinWallet
            game_transactions = PlayGameTransaction.objects.filter(account = coin_wallet, update_timestamp__gt = yesterday, update_timestamp__lte = today)
            game_transactions_count = game_transactions.count()
            user.num_played_games = game_transactions_count
        except Exception as e:
            user.num_played_games = 0

    num_creat_today = userHistory.filter(last_login__gt = yesterday).filter(create_timestamp__lte = today).count()
    num_login_today = userHistory.filter(create_timestamp__gt = yesterday).filter(last_login__lte = today).count()

    paymentHistory = PaymentHistory.objects.filter(update_timestamp__gt = yesterday, update_timestamp__lte = today).filter(Q(type="payment_action_intent_succeeded") | Q(type="payment_action_intent_failed")).all()
    
    email = render_to_string(email_template_name, {"project_name": project_name, "num_creat_today": num_creat_today, "num_login_today": num_login_today,"today": today, "yesterday": yesterday, "userHistories": userHistory, "paymentHistories": paymentHistory})
    email_content = strip_tags(email)

    try:
        send_mail(email_title, email_content, 'Learn With Socrates',
                    email_receivers, fail_silently=False, html_message=email)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return email