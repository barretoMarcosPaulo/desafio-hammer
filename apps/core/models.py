from django.db import models



class Person(models.Model):
    name = models.CharField("Nome do participante", max_length=255, blank=False, null=False)
    username = models.CharField("Nome de usuário", max_length=50, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
    
    def __str__(self):
        return self.name



class HammerBarbecue(models.Model):
    host = models.ForeignKey(Person, on_delete=models.PROTECT, blank=False, null=False)
    date = models.DateField("Data do churrasco", blank=False, null=False)
    location = models.CharField("Nome do participante", max_length=255, blank=False , null=False)
    spent_drinks = models.FloatField("Valor gasto em bebidas", default=0.0, blank=True , null=True)
    spent_foods = models.FloatField("Valor gasto em comida", default=0.0, blank=True , null=True)

    class Meta:
        verbose_name = 'Churrasco da Hammer'
        verbose_name_plural = 'Churrascos da Hammer'
    
    def __str__(self):
        return "{}-{}".format(str(self.date), self.location )



class Invitation(models.Model):
    participant = models.ForeignKey(Person, on_delete=models.PROTECT, blank=False, null=False)
    consumes_alcohol = models.BooleanField("Vai consumir alcool", default=True)
    guest = models.CharField("Nome do convidado", max_length=255, blank=True, null=True)
    presence = models.BooleanField("Presença no churrasco", default=False)
    contribution  = models.FloatField("Valor a contribuir", default=20)

    barbecue = models.ForeignKey(HammerBarbecue, on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = 'Convite'
        verbose_name_plural = 'convites'
    
    # def __str__(self):        
    #     return self.participant


