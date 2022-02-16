import calendar
import datetime
import os
import sys
from decimal import Decimal

import graphene
from django.db import transaction, DatabaseError
from django.utils import timezone
from graphene import ID
from payments.models import PaymentMethod
from students.models import Student
from .models import Plan, GuardianStudentPlan
from guardians.models import Guardian
from kb.models import AreaOfKnowledge
from app.utils import add_months
import payments.services as payment_services


class OrderDetailInput:
    guardian_student_plan_id: int
    plan_id: int
    quantity: int
    total: Decimal
    period: str

    def __init__(self, plan_id, quantity, total, period, guardian_student_plan_id=None):
        self.guardian_student_plan_id = guardian_student_plan_id
        self.plan_id = plan_id
        self.quantity = quantity
        self.total = total
        self.period = period


# Create new GuardianStudentPlan
class CreateGuardianStudentPlan(graphene.Mutation):
    guardian_student_plan = graphene.Field('plans.schema.GuardianStudentPlanSchema')
    order = graphene.Field('payments.schema.OrderSchema')
    url_redirect = graphene.String()

    class Arguments:
        guardian_id = graphene.ID(required=True)
        plan_id = graphene.ID(required=True)
        list_subject_id = graphene.List(ID)
        period = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        student_id = graphene.ID(required=False)
        return_url = graphene.String(required=True)

    def mutate(
            self,
            info,
            guardian_id,
            plan_id,
            list_subject_id,
            period,
            price,
            return_url,
            student_id=None
    ):
        try:
            with transaction.atomic():
                guardian = Guardian.objects.get(pk=guardian_id)
                plan = Plan.objects.get(pk=plan_id)

                if period != "Monthly" and period != "Yearly":
                    raise Exception("period must be Monthly or Yearly.")

                guardian_student_plan = GuardianStudentPlan.objects.create(
                    guardian_id=guardian.id,
                    plan_id=plan.id,
                    period=period,
                    price=price,
                    is_paid=False
                )

                guardian_student_plan.save()

                # list of subject
                if guardian_student_plan.plan.area_of_knowledge == "ALL":
                    subjects = AreaOfKnowledge.objects.all()
                    for subject in subjects:
                        guardian_student_plan.subject.add(subject)
                elif len(list_subject_id) != 0:
                    for subject_id in list_subject_id:
                        subject = AreaOfKnowledge.objects.get(pk=subject_id)
                        guardian_student_plan.subject.add(subject)

                if student_id:
                    student = Student.objects.get(pk=student_id)
                    guardian_student_plan.student_id = student.id

                guardian_student_plan.save()

                payment_method = PaymentMethod.objects.get(guardian_id=guardian_student_plan.guardian.id,
                                                           is_default=True)
                order_detail_input = OrderDetailInput(
                    plan_id=guardian_student_plan.plan_id,
                    quantity=1,
                    total=price,
                    period=period,
                    guardian_student_plan_id=guardian_student_plan.id
                )
                create_order_resp = payment_services.create_order(
                    guardian_id=guardian_student_plan.guardian.id,
                    discount=0,
                    discount_code="",
                    sub_total=price,
                    total=price,
                    payment_method=payment_method.method,
                    return_url=return_url,
                    order_detail_input=[order_detail_input]
                )

                return CreateGuardianStudentPlan(
                    guardian_student_plan=guardian_student_plan,
                    order=create_order_resp.order,
                    url_redirect=create_order_resp.url_redirect
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Update plan from yearly to monthly or another way around
class UpdateGuardianStudentPlan(graphene.Mutation):
    guardian_student_plan = graphene.Field('plans.schema.GuardianStudentPlanSchema')
    order = graphene.Field('payments.schema.OrderSchema')
    url_redirect = graphene.String()

    class Arguments:
        guardian_student_plan_id = graphene.ID(required=True)
        period = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        return_url = graphene.String(required=True)

    def mutate(
            self,
            info,
            guardian_student_plan_id,
            period,
            price,
            return_url
    ):
        try:
            with transaction.atomic():
                guardian_student_plan = GuardianStudentPlan.objects.get(pk=guardian_student_plan_id)

                if period != "Monthly" and period != "Yearly":
                    raise Exception("period must be Monthly or Yearly.")
                #
                # guardian_student_plan.period = period
                # guardian_student_plan.price = price
                #
                # if period == "Monthly":
                #     expired_date = add_months(datetime.datetime.now(), 1)
                # else:
                #     expired_date = add_months(datetime.datetime.now(), 12)
                #
                # guardian_student_plan.expired_at = expired_date
                # guardian_student_plan.is_paid = True
                #
                # guardian_student_plan.save()
                payment_method = PaymentMethod.objects.get(guardian_id=guardian_student_plan.guardian.id, is_default=True)
                order_detail_input = OrderDetailInput(
                    plan_id=guardian_student_plan.plan_id,
                    quantity=1,
                    total=price,
                    period=period,
                    guardian_student_plan_id=guardian_student_plan.id
                )
                create_order_resp = payment_services.create_order(
                    guardian_id=guardian_student_plan.guardian.id,
                    discount=0,
                    discount_code="",
                    sub_total=price,
                    total=price,
                    payment_method=payment_method.method,
                    return_url=return_url,
                    order_detail_input=[order_detail_input]
                )

                return UpdateGuardianStudentPlan(
                    guardian_student_plan=guardian_student_plan,
                    order=create_order_resp.order,
                    url_redirect=create_order_resp.url_redirect
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Cancel plan with reason
class CancelGuardianStudentPlan(graphene.Mutation):
    guardian_student_plan = graphene.Field('plans.schema.GuardianStudentPlanSchema')

    class Arguments:
        guardian_student_plan_id = graphene.ID(required=True)
        reason = graphene.String(required=True)

    def mutate(
            self,
            info,
            guardian_student_plan_id,
            reason):
        try:
            with transaction.atomic():
                guardian_student_plan = GuardianStudentPlan.objects.get(pk=guardian_student_plan_id)
                guardian_student_plan.cancel_reason = reason
                guardian_student_plan.is_cancel = True
                guardian_student_plan.update_timestamp = timezone.now()
                guardian_student_plan.save()

                return CancelGuardianStudentPlan(
                    guardian_student_plan=guardian_student_plan
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Cancel all the membership
class CancelMembership(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        guardian_id = graphene.ID(required=True)
        reason = graphene.String(required=True)

    def mutate(
            self,
            info,
            guardian_id,
            reason):
        try:
            with transaction.atomic():
                guardian = Guardian.objects.get(pk=guardian_id)
                guardian_student_plans = GuardianStudentPlan.objects.filter(guardian_id=guardian.id)
                for guardian_student_plan in guardian_student_plans:
                    guardian_student_plan.is_cancel = True
                    guardian_student_plan.cancel_reason = reason
                    guardian_student_plan.update_timestamp = timezone.now()
                    guardian_student_plan.save()

                return CancelMembership(
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


class Mutation(graphene.ObjectType):
    create_guardian_student_plan = CreateGuardianStudentPlan.Field()
    update_guardian_student_plan = UpdateGuardianStudentPlan.Field()
    cancel_guardian_student_plan = CancelGuardianStudentPlan.Field()
    cancel_membership = CancelMembership.Field()
