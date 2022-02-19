from django.contrib.auth import get_user_model
from api.models import profile
from graphql_jwt.shortcuts import create_refresh_token, get_token
from students.models import Student
from guardians.models import Guardian, GuardianStudent
from users.schema import UserSchema, UserProfileSchema
from users.models import User
from bank.models import Interest
import graphene
from datetime import datetime
from accounting.models import BankMovement
from accounting.models import Account
# TODO: move to user mutations
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)

    def mutate(self, info, username, password):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        user.save()

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, profile=profile_obj, token=token, refresh_token=refresh_token)


# TODO: move to guardian mutations
class CreateGuardian(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        if email is not None:
            user.email = email
        user.save()

        guardian = Guardian(
            user=user,
        )
        guardian.save()

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateGuardian(
            guardian=guardian,
            user=user, profile=profile_obj,
            token=token,
            refresh_token=refresh_token
        )


# TODO: move to guardian student mutations
class CreateGuardianStudent(graphene.Mutation):
    guardian_student = graphene.List('guardians.schema.GuardianStudentSchema')

    class Arguments:
        guardian = graphene.ID(required=True)
        students = graphene.List(graphene.NonNull(graphene.ID))

    def mutate(self, info, guardian, students):
        guardian = Guardian.objects.get(id=guardian)
        guardian_students = []

        for student_id in students:
            student = Student.objects.get(id=student_id)
            guardian_student = GuardianStudent(
                guardian=guardian,
                student=student
            )
            guardian_student.save()
            guardian_students.append(guardian_student)

        return CreateGuardianStudent(
            guardian_student=guardian_students,
        )


# TODO: move to guardian mutations
class ChangeGuardianEmailPassword(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=False)
        email = graphene.String(required=False)

    def mutate(self, info, username, password, email):
        user = User.objects.get(username=username)
        if password is not None and password != "":
            user.set_password(password)
        if email is not None and email != "":
            user.email = email
        user.save()

        guardian = Guardian.objects.get(user_id=user.id)

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return ChangeGuardianEmailPassword(
            guardian=guardian,
            user=user, profile=profile_obj,
            token=token,
            refresh_token=refresh_token
        )


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_guardian = CreateGuardian.Field()
    create_guardian_student = CreateGuardianStudent.Field()
    change_guardian_email_password = ChangeGuardianEmailPassword.Field()


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserSchema)
    users = graphene.List(UserSchema)

    def resolve_whoami(root, info, **kwargs):
        user = info.context.user
        if user.student:
            student = user.student
            now = datetime.now().date()
            delta =( now - student.int_period_start_at ).total_seconds() / 3600 / 24
            bankBallance = student.bankWallet.balance
            interests = Interest.objects.filter(period__lte=delta, requireCoin__lte=bankBallance
            ).order_by('-requireCoin')
            print(student.int_period_start_at, interests)
            if(len(interests) > 0) :
                amount = interests[0].amount
                # user.student.bankWallet.balance += amount
                BankMovement.objects.create(amount=amount, account=student.bankWallet, side=Account.SIDE_CHOICE_RIGHT_INTEREST)
        if user.is_anonymous:
            raise Exception('Authentication Failure')
        return user

    def resolve_users(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure')
        if user.profile.role != 'manager':
            raise Exception('Role Failure')
        return get_user_model().objects.all()
