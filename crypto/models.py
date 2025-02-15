from django.db import models

# Create your models here.
from django.db import models

class Exchange(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.URLField()

    def __str__(self):
        return self.name
    

class Price(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.price} on {self.exchange.name}"
    
class ArbitrageOpportunity(models.Model):
    symbol = models.CharField(max_length=20)
    buy_exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='buy_opportunities')
    buy_price = models.FloatField()
    sell_exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='sell_opportunities')
    sell_price = models.FloatField()
    profit_percentage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol}: Buy on {self.buy_exchange.name} and sell on {self.sell_exchange.name}"
