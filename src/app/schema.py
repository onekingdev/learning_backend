import graphene
import graphql_jwt
import achievements.schema
import api.schema
import audiences.schema
import block.schema
import collectibles.schema
import emails.schema
import experiences.schema
import guardians.schema
import kb.schema
import organization.schema
import plans.schema
import students.schema
import universals.schema


class Mutation(
        api.schema.Mutation,
        collectibles.schema.Mutation,
        emails.schema.Mutation,
        graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()


class Query(
        achievements.schema.Query,
        api.schema.Query,
        audiences.schema.Query,
        block.schema.Query,
        collectibles.schema.Query,
        experiences.schema.Query,
        guardians.schema.Query,
        kb.schema.Query,
        organization.schema.Query,
        plans.schema.Query,
        students.schema.Query,
        universals.schema.Query,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
