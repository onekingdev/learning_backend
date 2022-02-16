from app.utils import add_months
from guardians.models import Guardian
from payments.card import Card
from payments.models import Order, OrderDetail, PaypalTransaction, PaymentMethod, CardTransaction
from payments.paypal import Paypal
from plans.models import Plan, GuardianStudentPlan


class CreateOrderResp:
    url_redirect: str
    order: Order

    def __init__(self, url_redirect: str, order: Order):
        self.url_redirect = url_redirect
        self.order = order


def add_or_update_payment_method(method: str, guardian_id):
    payment_methods = PaymentMethod.objects.filter(guardian_id=guardian_id)

    if payment_methods.count() > 0:
        obj = PaymentMethod.objects.get(pk=payment_methods[0].id)
        print(obj.method, method)
        obj.method = method
        obj.save()
        return

    PaymentMethod.objects.create(
        guardian_id=guardian_id,
        method=method,
        is_default=True
    )
    return


def create_order(guardian_id,
                 discount_code,
                 discount,
                 sub_total,
                 total,
                 payment_method,
                 order_detail_input,
                 return_url) -> CreateOrderResp:

    guardian = Guardian.objects.get(pk=guardian_id)

    if payment_method != "Card" and payment_method != "PayPal" and payment_method != "ApplePay":
        raise Exception("need payment method enum Card, PayPal, ApplePay.")

    order = Order.objects.create(
        guardian_id=guardian.id,
        sub_total=sub_total,
        discount_code=discount_code,
        discount=discount,
        total=total,
        payment_method=payment_method
    )

    for order_detail_element in order_detail_input:
        plan = Plan.objects.get(pk=order_detail_element.plan_id)
        guardian_student_plan_id = None
        if order_detail_element.guardian_student_plan_id:
            guardian_student_plan_id = order_detail_element.guardian_student_plan_id
        OrderDetail.objects.create(
            guardian_student_plan_id=guardian_student_plan_id,
            plan_id=plan.id,
            quantity=order_detail_element.quantity,
            total=order_detail_element.total,
            order_id=order.id,
            period=order_detail_element.period
        )

    url_redirect = ""
    if order.payment_method == "PayPal":
        paypal = Paypal()
        paypal.get_token()
        paypal.check_out(return_url=return_url, cancel_url=return_url, value=order.total)
        PaypalTransaction.objects.create(
            order_id=order.id,
            token_id=paypal.token_id,
            approve_link=paypal.approve_link,
            capture_link=paypal.capture_link
        )
        url_redirect = paypal.approve_link
    elif order.payment_method == "Card":
        card = Card()
        card.create_session(return_url=return_url, total=order.total)
        CardTransaction.objects.create(
            order_id=order.id,
            session_id=card.session_id,
            approve_link=card.url_redirect
        )
        url_redirect = card.url_redirect

    return CreateOrderResp(url_redirect=url_redirect, order=order)


def confirm_order_payment(order_id) -> Order:
    order = Order.objects.get(pk=order_id)

    if order.is_paid:
        raise Exception("This order already been paid.")

    # Confirm payment by method type
    if order.payment_method == "PayPal":
        paypal_tx = PaypalTransaction.objects.get(order_id=order.id)
        paypal = Paypal()
        paypal.get_token()
        paypal.capture(paypal_tx)
    elif order.payment_method == "Card":
        card_tx = CardTransaction.objects.get(order_id=order.id)
        card = Card()
        card.check_session(card_tx)

    # change order paid status to true
    order.is_paid = True
    order.save()

    # create GuardianStudentPlan if payment is complete
    order_details = OrderDetail.objects.filter(order_id=order.id)
    for order_detail in order_details:
        if order_detail.guardian_student_plan is None:
            # create GuardianStudentPlan
            for package_amount in range(0, order_detail.quantity):
                guardian_student_plan = GuardianStudentPlan.objects.create(
                    guardian_id=order.guardian.id,
                    plan_id=order_detail.plan.id,
                    period=order_detail.period,
                    price=order_detail.total,
                    is_paid=True
                )
        else:
            # update GuardianStudentPlan if have foreignkey
            guardian_student_plan = GuardianStudentPlan.objects.get(pk=order_detail.guardian_student_plan.id)
            guardian_student_plan.price = order_detail.total
            guardian_student_plan.period = order_detail.period
            guardian_student_plan.is_paid = True

        # set expired date
        if guardian_student_plan.period == "Monthly":
            expired_date = add_months(guardian_student_plan.create_timestamp, 1)
        else:
            expired_date = add_months(guardian_student_plan.create_timestamp, 12)

        guardian_student_plan.expired_at = expired_date
        guardian_student_plan.save()

    return order
