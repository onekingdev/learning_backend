import graphene
from user.schema import UserSchema


class ChangeLanguage(graphene.Mutation):
    user = graphene.Field(UserSchema)

    class Arguments:
        language = graphene.String()

    def mutate(self, info, language):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")

        user.language = language
        user.save()

        return ChangeLanguage(user=user)


class Mutation(graphene.ObjectType):
    change_language = graphene.Field(ChangeLanguage)
