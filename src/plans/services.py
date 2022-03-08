from app.utils import add_months
from payments.models import Order, OrderDetail
from .models import GuardianStudentPlan


def create_guardian_student_plan(order: Order):
    # create GuardianStudentPlan if payment is complete
    order_details = OrderDetail.objects.filter(order_id=order.id)
    for order_detail in order_details:
        # if order_detail.guardian_student_plan is None:
        # create GuardianStudentPlan
        for package_amount in range(0, order_detail.quantity):
            guardian_student_plan = GuardianStudentPlan.objects.create(
                order_detail_id=order_detail.id,
                guardian_id=order.guardian.id,
                plan_id=order_detail.plan.id,
                period=order_detail.period,
                price=order_detail.total,
                is_paid=True
            )
            if guardian_student_plan.period == "Monthly":
                expired_date = add_months(guardian_student_plan.create_timestamp, 1)
            else:
                expired_date = add_months(guardian_student_plan.create_timestamp, 12)

            guardian_student_plan.expired_at = expired_date
            guardian_student_plan.save()
        # else:
        #     # update GuardianStudentPlan if have foreignkey
        #     guardian_student_plan = GuardianStudentPlan.objects.get(pk=order_detail.guardian_student_plan.id)
        #     guardian_student_plan.price = order_detail.total
        #     guardian_student_plan.period = order_detail.period
        #     guardian_student_plan.is_paid = True

        # set expired date
        # if guardian_student_plan.period == "Monthly":
        #     expired_date = add_months(guardian_student_plan.create_timestamp, 1)
        # else:
        #     expired_date = add_months(guardian_student_plan.create_timestamp, 12)
        #
        # guardian_student_plan.expired_at = expired_date
        # guardian_student_plan.save()