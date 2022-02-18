import graphene
import graphql_jwt
import achievements.schema
import api.schema
import audiences.schema
import block.schema
import block.mutations
import collectibles.schema
import collectibles.mutations
import emails.schema
import experiences.schema
import guardians.schema
import kb.schema
import organization.schema
import plans.schema
import students.schema
import students.mutations
import universals.schema
import users.schema
import wallets.schema
import avatars.schema
import avatars.mutations
import plans.mutations
import payments.mutations
import payments.schema


class Mutation(
        api.schema.Mutation,
        block.mutations.Mutation,
        students.mutations.Mutation,
        collectibles.mutations.Mutation,
        emails.schema.Mutation,
        avatars.mutations.Mutation,
        plans.mutations.Mutation,
        payments.mutations.Mutation,
        graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()


class Query(
        achievements.schema.Query,
        payments.schema.Query,
        api.schema.Query,
        audiences.schema.Query,
        block.schema.Query,
        collectibles.schema.Query,
        experiences.schema.Query,
        guardians.schema.Query,
        kb.schema.Query,
        organization.schema.Query,
        plans.schema.Query,
        users.schema.Query,
        students.schema.Query,
        avatars.schema.Query,
        universals.schema.Query,
        wallets.schema.Query,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
