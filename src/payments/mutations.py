import os
import sys
import graphene
from django.db import transaction, DatabaseError
from payments import services


class OrderDetailInput(graphene.InputObjectType):
    guardian_student_plan_id = graphene.ID()
    plan_id = graphene.ID()
    quantity = graphene.Int()
    total = graphene.Decimal()
    period = graphene.String()


# Create new order
class CreateOrder(graphene.Mutation):
    order = graphene.Field('payments.schema.OrderSchema')
    status = graphene.String()
    url_redirect = graphene.String()

    class Arguments:
        guardian_id = graphene.ID(required=True)
        discount_code = graphene.String(required=True)
        discount = graphene.Decimal(required=True)
        sub_total = graphene.Decimal(required=True)
        total = graphene.Decimal(required=True)
        payment_method = graphene.String(required=True)
        order_detail_input = graphene.List(OrderDetailInput)
        return_url = graphene.String(required=True)

    def mutate(
            self,
            info,
            guardian_id,
            discount_code,
            discount,
            sub_total,
            total,
            payment_method,
            order_detail_input,
            return_url
    ):
        try:
            with transaction.atomic():

                create_order_resp = services.create_order(guardian_id, discount_code, discount, sub_total, total, payment_method, order_detail_input, return_url)

                return CreateOrder(
                    order=create_order_resp.order,
                    status="success",
                    url_redirect=create_order_resp.url_redirect
                )
        except (Exception, DatabaseError) as e:
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

                # add payment method to guardian if it new one
                services.add_or_update_payment_method(order.payment_method, order.guardian.id)

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

    def mutate(
            self,
            info,
            guardian_id,
            method
    ):
        try:
            with transaction.atomic():

                services.add_or_update_payment_method(method, guardian_id)

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
