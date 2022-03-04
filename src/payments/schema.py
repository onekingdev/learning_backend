import graphene
from graphene_django import DjangoObjectType
from .models import Order, OrderDetail, PaymentMethod


class PaymentMethodSchema(DjangoObjectType):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class OrderDetailSchema(DjangoObjectType):
    class Meta:
        model = OrderDetail
        fields = "__all__"


class OrderSchema(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

        order_detail = graphene.List(OrderDetailSchema)

        def resolve_order_detail(self, info):
            order_detail_list = OrderDetail.objects.filter(order_id=self.id)
            return order_detail_list


class Query(graphene.ObjectType):
    # ----------------- Order ----------------- #
    orders = graphene.List(OrderSchema)
    order_by_id = graphene.Field(OrderSchema, id=graphene.String())

    def resolve_orders(self, info, **kwargs):
        # Querying a list
        return Order.objects.all()

    def resolve_order_by_id(self, info, id):
        # Querying a single question
        return Order.objects.get(pk=id)

    # ----------------- Payment Method ----------------- #
    payment_methods = graphene.List(PaymentMethodSchema)
    payment_method_id = graphene.Field(PaymentMethodSchema, id=graphene.String())

    def resolve_payment_methods(self, info, **kwargs):
        # Querying a list
        return PaymentMethod.objects.all()

    def resolve_payment_method_id(self, info, id):
        # Querying a single question
        return PaymentMethod.objects.get(pk=id)
