from students.models import Student
from block.models import BlockQuestionPresentation
from django.db.models import Count, F, Value
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from games.models import PlayGameTransaction
from payments.models import PaymentHistory
from users.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from app.services import encrypt, decrypt
def send_report_mail(send=True):
    print("===========Starting Send Report Email / "+timezone.now().strftime("%Y/%m/%d, %H:%M:%S")+"=============" )
    email_title = "Report"
    email_template_name = "emails/report/index.html"
    email_receivers = settings.REPORT_EMAIL_RECEIVERS
    project_name = "Prod Server" if settings.IS_PRODUCTION else "Dev Server"

    today = timezone.now()
    yesterday = today - timedelta(days=1)
    userHistory = (User.objects
        .filter((Q(create_timestamp__gt = yesterday) & Q(create_timestamp__lte = today)) | (Q(last_login__gt = yesterday) & Q(last_login__lte = today)))
        .annotate(num_correct_questions=Count('student__studentblockquestionpresentationhistory__block_question_presentation__id', distinct=True, filter=(Q(student__user__id=F("id")) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__status=BlockQuestionPresentation.STATUS_CORRECT) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__status=BlockQuestionPresentation.STATUS_CORRECT) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__update_timestamp__gt=yesterday) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__update_timestamp__lte=today))))
        .annotate(num_wrong_questions=Count('student__studentblockquestionpresentationhistory__block_question_presentation__id', distinct=True, filter=(Q(student__user__id=F("id")) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__status=BlockQuestionPresentation.STATUS_INCORRECT) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__update_timestamp__gt=yesterday) & Q(student__studentblockquestionpresentationhistory__block_question_presentation__update_timestamp__lte=today))))
        .annotate(num_purchased_collectibles=Count('student__studentcollectible__id', distinct=True, filter=Q(student__user__id=F("id")) & Q(student__studentcollectible__update_timestamp__gt=yesterday) & Q(student__studentcollectible__update_timestamp__lte=today)))
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
    #-------------------- Get Payment History -S---------------------#
    paymentHistory = PaymentHistory.objects.filter(update_timestamp__gt = yesterday, update_timestamp__lte = today).filter(Q(type="payment_action_intent_succeeded") | Q(type="payment_action_intent_failed")).all()
    #-------------------- Get Payment History -E---------------------#
    
    #-------------------- Get Universal Password -S-------------------#
    now = datetime.now()
    format = "%Y-%m-%d %H:%M:%S"
    universal_password = encrypt(datetime.strftime((now),format))
    print("universal password is", universal_password)
    #-------------------- Get Universal Password -E-------------------#

    email = render_to_string(email_template_name, {"project_name": project_name, "num_creat_today": num_creat_today, "num_login_today": num_login_today,"today": today, "yesterday": yesterday, "userHistories": userHistory, "paymentHistories": paymentHistory, "universal_password": universal_password})
    email_content = strip_tags(email)



    if(send == True):
        try:
            send_mail(email_title, email_content, 'Learn With Socrates',
                        email_receivers, fail_silently=False, html_message=email)
        except Exception as e:
            print(e)
            # return {"email":email, "universal_password": universal_password, "num_creat_today": num_creat_today, "num_login_today": num_login_today,"today": today, "yesterday": yesterday, "userHistories": userHistory, "paymentHistories": paymentHistory, "success": False, "message": [{"tags":"error","message":str(e)}]}

    print("===========Finishing Send Report Email / "+timezone.now().strftime("%Y/%m/%d, %H:%M:%S")+"=============" )
    
    return {"email":email, "universal_password": universal_password, "num_creat_today": num_creat_today, "num_login_today": num_login_today,"today": today, "yesterday": yesterday, "userHistories": userHistory, "paymentHistories": paymentHistory, "success": True, "message": [{"message":"Report Email has been successfully sent!"}],}