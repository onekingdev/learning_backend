from django.db import models
from app.models import RandomSlugModel, TimestampModel


class Account(RandomSlugModel, TimestampModel):
    calculated_fields = ['balance']

    SIDE_CHOICE_LEFT = 'L'
    SIDE_CHOICE_RIGHT = 'R'
    SIDE_CHOICE_SET = (
        (SIDE_CHOICE_LEFT, 'Left'),
        (SIDE_CHOICE_RIGHT, 'Right'),
    )

    name = models.CharField(max_length=128)
    positive_side = models.CharField(default=SIDE_CHOICE_RIGHT, choices=SIDE_CHOICE_SET,
                                     max_length=16, )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.set_calculated_fields()
        super().save(*args, **kwargs)

    def set_calculated_fields(self):
        for field_name in self.calculated_fields:
            setattr(self, field_name, getattr(self, 'get_' + field_name)())

    @property
    def get_positive_side(self):
        return self.positive_side

    @property
    def get_negative_side(self):
        return {
            self.SIDE_CHOICE_LEFT: self.SIDE_CHOICE_RIGHT,
            self.SIDE_CHOICE_RIGHT: self.SIDE_CHOICE_LEFT
        }[self.positive_side]

    def get_balance_aggregate(self):
        positive_movements_aggregate = self.movement_set.filter(
            side=self.positive_side).aggregate(models.Sum('amount'))
        negative_movements_aggregate = self.movement_set.filter(side=self.get_negative_side).aggregate(
            models.Sum('amount'))

        positive_movements_balance = positive_movements_aggregate['amount__sum'] if positive_movements_aggregate[
            'amount__sum'] else 0
        negative_movements_balance = negative_movements_aggregate['amount__sum'] if negative_movements_aggregate[
            'amount__sum'] else 0

        dict = {}
        # balance = positive_movements_balance - negative_movements_balance
        balance = positive_movements_balance - negative_movements_balance
        dict['positive_movements_balance'] = positive_movements_balance
        dict['negative_movements_balance'] = negative_movements_balance
        dict['total_movements_balance'] = balance
        return dict

    def get_latest_movements(self, count_limit=40):
        movements = self.movement_set.filter()[:count_limit]
        return movements

    def get_balance(self):
        return self.get_balance_aggregate().get('total_movements_balance')


class Movement(RandomSlugModel, TimestampModel):
    class Meta:
        ordering = ['-date', '-pk']

    account = models.ForeignKey(
        'wallets.CoinWallet', on_delete=models.CASCADE, verbose_name='Cuenta')
    date = models.DateField('Fecha Movimiento', auto_now_add=True)
    side = models.CharField('Lado', max_length=1,
                            choices=Account.SIDE_CHOICE_SET)
    comment = models.CharField(
        'Comentario', max_length=128, null=True, blank=True, )
    amount = models.DecimalField('Monto', decimal_places=2, max_digits=11)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        account = self.account
        account.save()

    def delete(self, *args, **kwargs):
        account = self.account
        super(Movement, self).delete(*args, **kwargs)
        account.save()


class PositiveMovement(Movement):
    class Meta:
        proxy = True,

    def save(self, *args, **kwargs):
        self.side = self.account.get_positive_side
        return super().save(*args, **kwargs)


class NegativeMovement(Movement):
    class Meta:
        proxy = True,

    def save(self, *args, **kwargs):
        self.side = self.account.get_negative_side
        return super().save(*args, **kwargs)


''' 
Bank Wallet Implementation

'''

class BankMovement(RandomSlugModel, TimestampModel):
    class Meta:
        ordering = ['-date', '-pk']

    account = models.ForeignKey(
        'bank.BankWallet', on_delete=models.CASCADE, verbose_name='Cuenta')
    date = models.DateField('Fecha Movimiento', auto_now_add=True)
    side = models.CharField('Lado', max_length=1,
                            choices=Account.SIDE_CHOICE_SET)
    comment = models.CharField(
        'Comentario', max_length=128, null=True, blank=True, )
    amount = models.DecimalField('Monto', decimal_places=2, max_digits=11)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        account = self.account
        account.save()

    def delete(self, *args, **kwargs):
        account = self.account
        super(BankMovement, self).delete(*args, **kwargs)
        account.save()


class BankPositiveMovement(BankMovement):
    def save(self, *args, **kwargs):
        self.side = self.account.get_positive_side
        return super().save(*args, **kwargs)


class BankNegativeMovement(BankMovement):

    def save(self, *args, **kwargs):
        self.side = self.account.get_negative_side
        return super().save(*args, **kwargs)
