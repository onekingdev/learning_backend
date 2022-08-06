import os
import sys
import graphene
from django.db import transaction, DatabaseError
from guardians.models import Guardian
from organization.models.schools import SchoolSubscriber, SchoolTeacher, TeacherClassroom
from organization.schema import AdministrativePersonnelSchema, SubscriberSchema, TeacherSchema
from payments import services
from payments.card import Card
from plans import services as plan_services
from plans.models import GuardianStudentPlan
from students.schema import StudentSchema
from .models import Order, OrderDetail, PaymentHistory, PaymentMethod
from users.models import User
from django.utils import timezone

class OrderDetailInput(graphene.InputObjectType):
    plan_id = graphene.ID()
    quantity = graphene.Int()
    period = graphene.String()


# Create new order
class CreateOrder(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    teacher = graphene.Field('organization.schema.TeacherSchema')
    school = graphene.Field('organization.schema.SchoolSchema')
    order = graphene.Field('payments.schema.OrderSchema')
    status = graphene.String()
    url_redirect = graphene.String()

    class Arguments:
        guardian_id = graphene.ID(required=False)
        teacher_id = graphene.ID(required=False)
        school_id = graphene.ID(required=False)
        payment_method = graphene.String(required=True)
        order_detail_input = graphene.List(OrderDetailInput)
        return_url = graphene.String(required=True)
        card_first_name = graphene.String(required=False)
        card_last_name = graphene.String(required=False)
        card_number = graphene.String(required=False)
        card_exp_month = graphene.String(required=False)
        card_exp_year = graphene.String(required=False)
        card_cvc = graphene.String(required=False)
        address1 = graphene.String(required=False)
        address2 = graphene.String(required=False)
        city = graphene.String(required=False)
        state = graphene.String(required=False)
        post_code = graphene.String(required=False)
        country = graphene.String(required=False)
        phone = graphene.String(required=False)

    def mutate(
            self,
            info,
            payment_method,
            order_detail_input,
            return_url,
            guardian_id = None,
            school_id = None,
            teacher_id = None,
            card_first_name=None,
            card_last_name=None,
            card_number=None,
            card_exp_month=None,
            card_exp_year=None,
            card_cvc=None,
            address1=None,
            address2=None,
            city=None,
            state=None,
            post_code=None,
            country=None,
            phone=None
    ):
        if guardian_id is not None :
            user = User.objects.get(guardian__id = guardian_id)
        elif teacher_id is not None:
            user = User.objects.get(schoolpersonnel__teacher__id = teacher_id)
        elif school_id is not None:
            user = SchoolSubscriber.objects.get(school_id = school_id).subscriber.user
        try:
            # with transaction.atomic():
                sub_total = 0
                discount = 0
                total = 0
                create_order_resp = services.create_order(
                    guardian_id=guardian_id,
                    school_id=school_id,
                    teacher_id=teacher_id,
                    discount_code=None,
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
                    card_last_name=card_last_name,
                    address1=address1,
                    address2=address2,
                    city=city,
                    state=state,
                    post_code=post_code,
                    country=country,
                    phone=phone
                )
                print("after create services")
                
                PaymentHistory.objects.create(
                    type = "backend_anction_order_create",
                    user = user,
                    order = create_order_resp.order
                )
                return CreateOrder(
                    guardian=create_order_resp.order.guardian,
                    teacher = create_order_resp.order.teacher,
                    school = create_order_resp.order.school,
                    order=create_order_resp.order,
                    status="success",
                    url_redirect=create_order_resp.url_redirect
                )
        except (Exception, AssertionError, DatabaseError) as e:
            # transaction.rollback()
            try:
                PaymentHistory.objects.create(
                    type = "backend_anction_order_create_error",
                    user = user,
                    message = str(e)
                )
            except Exception as err:
                print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Confirm order have been paid
class ConfirmPaymentOrder(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    teacher = graphene.Field('organization.schema.TeacherSchema')
    school = graphene.Field('organization.schema.SchoolSchema')
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
                print("finish confirm order")
                # plan_services.create_guardian_student_plan(order)
                print("finish create plan services")
                if order.guardian is not None:
                    user = order.guardian.user
                elif order.teacher is not None:
                    user = order.teacher.user
                elif order.school is not None:
                    school = order.school
                    user = SchoolSubscriber.objects.get(school = school).subscriber.user
                print("user is ", user)
                print("order is ", order)


                PaymentHistory.objects.create(
                    type = "backend_anction_confirm_payment_order",
                    user = user,
                    order = order
                )
                return ConfirmPaymentOrder(
                    guardian=order.guardian,
                    teacher=order.teacher,
                    school = order.school,
                    order=order,
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            print(str(e))
            try:
                order = Order.objects.get(pk = order_id)
                if order.guardian is not None:
                    user = order.guardian.user
                elif order.teacher is not None:
                    user = order.teacher.user
                elif order.school is not None:
                    school = order.school
                    
                    user = SchoolSubscriber.objects.get(school = school).subscriber.user
                PaymentHistory.objects.create(
                    type = "backend_anction_confirm_payment_order_error",
                    user = user,
                    order = order,
                    message = str(e)
                )
            except Exception as err:
                return err
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Add new payment
class ChangePaymentMethod(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
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
        address1 = graphene.String(required=False)
        address2 = graphene.String(required=False)
        city = graphene.String(required=False)
        state = graphene.String(required=False)
        post_code = graphene.String(required=False)
        country = graphene.String(required=False)
        phone = graphene.String(required=False)

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
            card_cvc=None,
            address1=None,
            address2=None,
            city=None,
            state=None,
            post_code=None,
            country=None,
            phone=None
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
                    card_last_name=last_name,
                    address1=address1,
                    address2=address2,
                    city=city,
                    state=state,
                    post_code=post_code,
                    country=country,
                    phone=phone
                )

                user = services.change_order_detail_payment_method(guardian_id=guardian_id)
                guardian = user.guardian
                PaymentHistory.objects.create(
                    type = "backend_anction_change_default_payment_method",
                    user = guardian.user,
                    card_number = card_number
                )
                return ChangePaymentMethod(
                    guardian=guardian,
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            try:
                PaymentHistory.objects.create(
                    type = "backend_anction_change_default_payment_method_error",
                    user = Guardian.objects.get(pk=guardian_id).user,
                    card_number = card_number,
                    message = str(e)
                )
            except Exception as err:
                return err
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Add new payment
class EditPaymentMethod(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    status = graphene.String()

    class Arguments:
        payment_method_id = graphene.ID(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        card_number = graphene.String(required=False)
        card_exp_month = graphene.String(required=False)
        card_exp_year = graphene.String(required=False)
        card_cvc = graphene.String(required=False)
        address1 = graphene.String(required=False)
        address2 = graphene.String(required=False)
        city = graphene.String(required=False)
        state = graphene.String(required=False)
        post_code = graphene.String(required=False)
        country = graphene.String(required=False)
        phone = graphene.String(required=False)


    def mutate(
            self,
            info,
            payment_method_id,
            first_name=None,
            last_name=None,
            card_number=None,
            card_exp_month=None,
            card_exp_year=None,
            card_cvc=None,
            address1=None,
            address2=None,
            city=None,
            state=None,
            post_code=None,
            country=None,
            phone=None
    ):
        try:
            with transaction.atomic():

                guardian_id = services.edit_payment_method(
                    payment_method_id=payment_method_id,
                    card_number=card_number,
                    card_exp_month=card_exp_month,
                    card_exp_year=card_exp_year,
                    card_cvc=card_cvc,
                    card_first_name=first_name,
                    card_last_name=last_name,
                    address1=address1,
                    address2=address2,
                    city=city,
                    state=state,
                    post_code=post_code,
                    country=country,
                    phone=phone
                )

                user = services.change_order_detail_payment_method(guardian_id=guardian_id)
                guardian = user.guardian
                PaymentHistory.objects.create(
                    type = "backend_anction_edit_payment_method",
                    user = guardian.user,
                    card_number = card_number
                )
                return ChangePaymentMethod(
                    guardian=guardian,
                    status="success"
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            try:
                PaymentHistory.objects.create(
                    type = "backend_anction_edit_payment_method_error",
                    user = PaymentMethod.objects.get(pk=payment_method_id).guardian.user,
                    card_number = card_number,
                    message = str(e)
                )
            except Exception as err:
                return err
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# Create new order with out pay
class CreateOrderWithOutPay(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    order = graphene.Field('payments.schema.OrderSchema')
    status = graphene.String()
    teacher = graphene.Field('organization.schema.TeacherSchema')
    school = graphene.Field('organization.schema.SchoolSchema')
    class Arguments:
        guardian_id = graphene.ID(required=False)
        teacher_id = graphene.ID(required=False)
        school_id = graphene.ID(required=False)
        order_detail_input = graphene.List(OrderDetailInput)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        address1 = graphene.String(required=False)
        address2 = graphene.String(required=False)
        city = graphene.String(required=False)
        state = graphene.String(required=False)
        post_code = graphene.String(required=False)
        country = graphene.String(required=False)
        phone = graphene.String(required=False)

    def mutate(
            self,
            info,
            order_detail_input,
            guardian_id=None,
            teacher_id=None,
            school_id=None,
            first_name=None,
            last_name=None,
            address1=None,
            address2=None,
            city=None,
            state=None,
            post_code=None,
            country=None,
            phone=None
    ):
        if guardian_id is not None :
            user = User.objects.get(guardian__id = guardian_id)
        elif teacher_id is not None:
            user = User.objects.get(schoolpersonnel__teacher__id = teacher_id)
        elif school_id is not None:            
            user = SchoolSubscriber.objects.get(school_id = school_id).subscriber.user
        try:
            with transaction.atomic():
                create_order_resp = services.create_order_with_out_pay(
                    guardian_id=guardian_id,
                    teacher_id = teacher_id,
                    school_id = school_id,
                    order_detail_list=order_detail_input,
                )
                services.confirm_order_payment(
                    create_order_resp.order.id,
                    first_name=first_name,
                    last_name=last_name,
                    address1=address1,
                    address2=address2,
                    city=city,
                    state=state,
                    post_code=post_code,
                    country=country,
                    phone=phone
                )
                PaymentHistory.objects.create(
                    type = "backend_anction_create_order_without_pay",
                    user = user,
                    order = create_order_resp.order,
                )
                return CreateOrderWithOutPay(
                    guardian=create_order_resp.order.guardian,
                    teacher=create_order_resp.order.teacher,
                    school =create_order_resp.order.school,
                    order=create_order_resp.order,
                    status="success",
                )
        except (Exception, AssertionError, DatabaseError) as e:
            transaction.rollback()
            try:
                
                PaymentHistory.objects.create(
                    type = "backend_anction_create_order_without_pay_error",
                    user = user,
                    message = str(e)
                )
            except Exception as err:
                print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CancelOrderdetailById(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    student = graphene.Field(StudentSchema)
    subscriber = graphene.Field(SubscriberSchema)
    teacher = graphene.Field(TeacherSchema)
    administrativepersonnel = graphene.Field(AdministrativePersonnelSchema)
    status = graphene.String()

    class Arguments:
        order_detail_id = graphene.ID(required=True)
        reason = graphene.String(required=True)

    def mutate(
            self,
            info,
            order_detail_id,
            reason):
        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                order_detail = OrderDetail.objects.get(pk=order_detail_id)

                old_payment = order_detail.order.payment_method

                if old_payment == "CARD":
                    card = Card()
                    sub = card.cancel_subscription(sub_id=order_detail.subscription_id)

                    if sub.status != "canceled":
                        raise Exception(f"cannot unsub order_detail_id {order_detail.id} from stripe")

                order_detail.status = "canceled"
                order_detail.cancel_reason = reason
                order_detail.is_cancel = True
                order_detail.update_timestamp = timezone.now()
                order_detail.save()

                # cancel guardian student plan
                guardian_student_plans = GuardianStudentPlan.objects.filter(order_detail_id=order_detail.id)
                for guardian_student_plan in guardian_student_plans:
                    guardian_student_plan.is_cancel = True
                    guardian_student_plan.cancel_reason = reason
                    guardian_student_plan.update_timestamp = timezone.now()
                    guardian_student_plan.save()

                teacher_classrooms = TeacherClassroom.objects.filter(order_detail_id=order_detail.id)
                for teacher_classroom in teacher_classrooms:
                    teacher_classroom.is_cancel = True
                    teacher_classroom.cancel_reason = reason
                    teacher_classroom.update_timestamp = timezone.now()
                    teacher_classroom.save()

                school_teachers = SchoolTeacher.objects.filter(order_detail_id=order_detail.id)
                for school_teacher in school_teachers:
                    school_teacher.is_cancel = True
                    school_teacher.cancel_reason = reason
                    school_teacher.update_timestamp = timezone.now()
                    school_teacher.save()

                guardian = user.guardian if hasattr(user, "guardian") else None
                student = user.student if hasattr(user, "student") else None
                subscriber = user.schoolpersonnel.subscriber if hasattr(user, "schoolpersonnel") and hasattr(user.schoolpersonnel, "subscriber") else None
                teacher = user.schoolpersonnel.teacher if hasattr(user, "schoolpersonnel") and hasattr(user.schoolpersonnel, "teacher") else None
                administrativepersonnel = user.schoolpersonnel.administrativepersonnel if hasattr(user, "schoolpersonnel") and hasattr(user.schoolpersonnel, "administrativepersonnel") else None

                return CancelOrderdetailById(
                    guardian = guardian,
                    student = student,
                    subscriber = subscriber,
                    teacher = teacher,
                    administrativepersonnel = administrativepersonnel,
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
    create_order_with_out_pay = CreateOrderWithOutPay.Field()
    confirm_payment_order = ConfirmPaymentOrder.Field()
    change_payment_method = ChangePaymentMethod.Field()
    edit_payment_method = EditPaymentMethod.Field()
    cancel_orderdetail_by_id = CancelOrderdetailById.Field()

