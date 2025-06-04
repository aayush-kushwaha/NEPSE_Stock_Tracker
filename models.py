from tortoise import fields
from tortoise.models import Model
from enum import Enum

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

class StockSource(str, Enum):
    IPO = "IPO"
    Secondary_Market = "Secondary Market"
    
class Portfolio(Model):
    id = fields.IntField(pk=True)  
    user = fields.ForeignKeyField("models.User", related_name="portfolios") # Now, every portfolio entry will belong to a user.
    stock_name = fields.CharField(max_length=10)
    total_shares = fields.IntField()
    purchase_rate = fields.FloatField()
    total_purchase_value = fields.FloatField()
    source = fields.CharEnumField(StockSource)
    purchase_date = fields.DateField()  
    created_at = fields.DatetimeField(auto_now_add=True)