import os
import sys
import graphene
from django.db import transaction, DatabaseError
from payments import services
from plans.models import Plan
from plans import services as plan_services


class OrderDetailInput(graphene.InputObjectType):
    plan_id = graphene.ID()
    quantity = graphene.Int()
    period = graphene.String()


# Create new order
class CreateOrder(graphene.Mutation):
    order = graphene.Field('payments.schema.OrderSchema')
    status = graphene.String()
    url_redirect = graphene.String()

    class Arguments:
        guardian_id = graphene.ID(required=True)
        discount_code = graphene.String(required=True)
        payment_method = graphene.String(required=True)
        order_detail_input = graphene.List(OrderDetailInput)
        return_url = graphene.String(required=True)
        card_first_name = graphene.String(required=False)
        card_last_name = graphene.String(required=False)
        card_number = graphene.String(required=False)
        card_exp_month = graphene.String(required=False)
        card_exp_year = graphene.String(required=False)
        card_cvc = graphene.String(required=False)

    def mutate(
            self,
            info,
            guardian_id,
            discount_code,
            payment_method,
            order_detail_input,
            return_url,
            card_first_name=None,
            card_last_name=None,
            card_number=None,
            card_exp_month=None,
            card_exp_year=None,
            card_cvc=None
    ):
        try:
            with transaction.atomic():
                sub_total = 0
                discount = 0
                total = 0
                create_order_resp = services.create_order(
                    guardian_id=guardian_id,
                    discount_code=discount_code,
                    discount=discount,
                    sub_total=sub_total,
                    total=total,
                    payment_method=payment_method,
                    order_detail_list=order_detail_input,
                    return_url=return_url,
                    card_number=card_number,
                    card_exp_month=card_exp_month,
                    card_exp_year=card_exp_year,
                    card_cvc=card_cvc,
                    card_first_name=card_first_name,
                    card_last_name=card_last_name
                )

                return CreateOrder(
                    order=create_order_resp.order,
                    status="success",
                    url_redirect=create_order_resp.url_redirect
                )
        except (Exception, AssertionError, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Confirm order have been paid
class ConfirmPaymentOrder(graphene.Mutation):
    order = graphene.Field('payments.schema.OrderSchema')
    status = graphene.String()

    class Arguments:
        order_id = graphene.ID(required=True)

    def mutate(
            self,
            info,
            order_id
    ):
        try:
            with transaction.atomic():

                order = services.confirm_order_payment(order_id)
                plan_services.create_guardian_student_plan(order)

                return ConfirmPaymentOrder(
                    order=order,
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Add new payment
class ChangePaymentMethod(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        guardian_id = graphene.ID(required=True)
        method = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        card_number = graphene.String(required=False)
        card_exp_month = graphene.String(required=False)
        card_exp_year = graphene.String(required=False)
        card_cvc = graphene.String(required=False)

    def mutate(
            self,
            info,
            guardian_id,
            method,
            first_name=None,
            last_name=None,
            card_number=None,
            card_exp_month=None,
            card_exp_year=None,
            card_cvc=None
    ):
        try:
            with transaction.atomic():

                services.change_default_payment_method(
                    guardian_id=guardian_id,
                    method=method,
                    card_number=card_number,
                    card_exp_month=card_exp_month,
                    card_exp_year=card_exp_year,
                    card_cvc=card_cvc,
                    card_first_name=first_name,
                    card_last_name=last_name
                )

                return ChangePaymentMethod(
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Add new payment
class EditPaymentMethod(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        payment_method_id = graphene.ID(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        card_number = graphene.String(required=False)
        card_exp_month = graphene.String(required=False)
        card_exp_year = graphene.String(required=False)
        card_cvc = graphene.String(required=False)

    def mutate(
            self,
            info,
            payment_method_id,
            first_name=None,
            last_name=None,
            card_number=None,
            card_exp_month=None,
            card_exp_year=None,
            card_cvc=None
    ):
        try:
            with transaction.atomic():

                services.edit_payment_method(
                    payment_method_id=payment_method_id,
                    card_number=card_number,
                    card_exp_month=card_exp_month,
                    card_exp_year=card_exp_year,
                    card_cvc=card_cvc,
                    card_first_name=first_name,
                    card_last_name=last_name
                )

                return ChangePaymentMethod(
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    confirm_payment_order = ConfirmPaymentOrder.Field()
    change_payment_method = ChangePaymentMethod.Field()
    edit_payment_method = EditPaymentMethod.Field()
