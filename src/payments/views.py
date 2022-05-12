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
from payments.models import OrderDetail
from plans.models import GuardianStudentPlan
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()
stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY if settings.STRIPE_LIVE_MODE == True else settings.STRIPE_TEST_SECRET_KEY

@csrf_exempt
def stripeWebHook(request):
    print("in stripe web hook")
    
    response_err = []
    try:

        sig = request.headers.get("stripe-signature");

        event = stripe.Webhook.construct_event(
            payload = request.body,
            sig_header = sig,
            secret = settings.STRIPE_LIVE_WEBHOOK_KEY if settings.STRIPE_LIVE_MODE == True else settings.STRIPE_TEST_WEBHOOK_KEY
            )
        # event = json.loads(request.body)

        intent = event['data']['object']
        now = datetime.datetime.now()

        # -------------- If payment is succeeded on stripe -S----------------#
        if(event['type'] == "payment_intent.succeeded"):
            customer_id = intent['charges']['data'][0]['customer']
            subscriptions = stripe.Subscription.list(customer=customer_id)['data']

            for subscription in subscriptions:
                try :
                    subscription_status = subscription['status']
                    subscription_end_at = datetime.datetime.fromtimestamp(subscription['current_period_end'])
                    print(subscription['current_period_end'])
                    # ---------- Get guardian student plan from subscription id -S----------------#
                    order_detail = OrderDetail.objects.get(subscription_id = subscription['id'])
                    # order_detail = OrderDetail.objects.get(subscription_id = "sub_1KqOQNAfwM01sssKrJfXOzrb")
                    # order_detail = OrderDetail.objects.get(pk=112)
                    # if(len(order_detail) < 1): 
                    #     continue;
                    # order_detail = order_detail[0]
                    guardian_student_plans = order_detail.guardianstudentplan_set.all()
                    print(guardian_student_plans, guardian_student_plans[0])
                    # ---------- Get guardian student plan from subscription id -E----------------#

                    # --------------- Get user by email from requedst -S---------------------#
                    # user = User.objects.filter(email = intent.charges.data[0].billing_details.email)
                    # if(len(user) < 1) :
                    #     return JsonResponse({"status": "error", "message": "Current user was deleted on database" })
                    # user = user[0]
                    # --------------- Get user by email from request -E---------------------#

                    # guardian = user.guardian
                    # guardianStudentPlans = guardian.guardianstudentplan_set

                    # --------------- Update Expire Date to after period days -S----------------- #
                    for guardian_student_plan in guardian_student_plans:
                        # period = 32 if guardian_student_plan.period == "MONTHLY" else 367
                        period =2
                        guardian_student_plan.is_paid = True if subscription_status == "active" or subscription_status == "incomplete" else False
                        guardian_student_plan.expired_at = subscription_end_at + datetime.timedelta(days=period)
                        guardian_student_plan.save()

                        guardian_student_plan.order_detail.is_paid = True if subscription_status == "active" or subscription_status == "incomplete" else False
                        guardian_student_plan.order_detail.expired_at = now + datetime.timedelta(days=period)
                        guardian_student_plan.order_detail.save()
                    # --------------- Update Expire Date to after period days -E----------------- #
                except Exception as e:
                    response_err.append("Subscription ID " + subscription['id'] + " : " + str(e))
            return JsonResponse({"status": "failed", "msg": response_err}) if len(response_err) > 0 else JsonResponse({"status": "success"})
        # -------------- If payment is succeeded on stripe -S----------------#

        # -------------- If payment is failed on stripe -S----------------#
        elif(event['type'] == "payment_intent.payment_failed"):
            message = intent['last_payment_error'] if intent['last_payment_error'] else intent['last_payment_error']['message'];
            customer_id = intent['charges']['data'][0]['customer']
            subscriptions = stripe.Subscription.list(customer=customer_id)

            for subscription in subscriptions:
                subscription_status = subscription.data.status
                subscription_end_at = datetime.datetime.fromtimestamp(subscription.data.current_period_end)
                # ---------- Get guardian student plan from subscription id -S----------------#
                order_detail = OrderDetail.objects.filter(subscription_id = subscription.data.id)
                order_detail = order_detail[0]
                guardian_student_plans = order_detail.guardianstudentplan_set
                # ---------- Get guardian student plan from subscription id -E----------------#

                # --------------- Get user by email from requedst -S---------------------#
                # user = User.objects.filter(email = intent.charges.data[0].billing_details.email)
                # if(len(user) < 1) :
                #     return JsonResponse({"status": "error", "message": "Current user was deleted on database" })
                # user = user[0]
                # --------------- Get user by email from request -E---------------------#

                # guardian = user.guardian
                # guardianStudentPlans = guardian.guardianstudentplan_set

                # --------------- Update Expire Date to after period days -S----------------- #
                for i, guardian_student_plan in guardian_student_plans:
                    # period = 32 if guardian_student_plans[i].period == "MONTHLY" else 367
                    period =2

                    guardian_student_plans[i].is_paid = True if subscription_status == "active" or subscription_status == "incomplete" else False
                    guardian_student_plans[i].expired_at = subscription_end_at + datetime.timedelta(days=period)
                    guardian_student_plans[i].save()

                    guardian_student_plans[i].order_detail.is_paid = True if subscription_status == "active" or subscription_status == "incomplete" else False
                    guardian_student_plans[i].order_detail.expiredAt = now + datetime.timedelta(days=period)
                    guardian_student_plans[i].order_detail.save()
                # --------------- Update Expire Date to after period days -E----------------- #
            
            return JsonResponse({"status": "success"})
        # -------------- If payment is failed on stripe -S----------------#
        else:
            return JsonResponse({"status": "failed", "msg": "unknown events"})

    except Exception as e:
        print(str(e))
        msg = str(e)
        return JsonResponse({"status": "failed", "msg": msg})


    


        