import json
import stripe
from django.http import HttpResponse
from django.core.files import File
from django.conf import settings
import lxml.html as LH
from graphql_jwt.utils import (jwt_decode, refresh_has_expired)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json

from django.http import HttpResponse
import os
import lxml.html as LH
from django.http import JsonResponse
import datetime
from django.conf import settings

User = get_user_model()

def stripeWebHook(request):
    
    sig = request.headers["stripe-signature"];
    
    event = stripe.Webhook.construct_event(
        request.body,
        sig,
        settings.STRIPE_LIVE_SECRET_KEY if settings.STRIPE_LIVE_MODE == True else settings.STRIPE_TEST_WEBHOOK_KEY
        )
    intent = event.data.object

    # -------------- If payment is succeeded on stripe -S----------------#
    if(event.type == "payment_intent.succeeded"):
        # --------------- Get user by email from requedst -S---------------------#
        user = User.objects.filter(email = intent.chages.data[0].billing_details.email)
        if(len(user) < 1) :
            return JsonResponse({"status": "error", "message": "Current user was deleted on database" })
        user = user[0]
        # --------------- Get user by email from requedst -E---------------------#

        guardian = user.guardian

        now = datetime.datetime.now()

        guardianStudentPlans = guardian.uardianstudentplan_set

        # --------------- Update Expire Date to after period days -S----------------- #
        for i,guardianStudentPlan in guardianStudentPlans:
            period = 32 if guardianStudentPlans[i].period == "MONTHLY" else 367

            guardianStudentPlans[i].is_paid = True
            guardianStudentPlans[i].expired_at = now + datetime.timedelta(days=now + period)
            guardianStudentPlans[i].save()

            guardianStudentPlans[i].order_detail.is_paid = True
            guardianStudentPlans[i].order_detail.expiredAt = now + datetime.timedelta(days=now + period)
            guardianStudentPlans[i].order_detail.save()
        # --------------- Update Expire Date to after period days -E----------------- #
        
        return JsonResponse({"status": "success"})

    # -------------- If payment is succeeded on stripe -S----------------#
    


        