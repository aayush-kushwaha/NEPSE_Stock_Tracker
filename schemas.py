from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class GetStockPrice(BaseModel):
    nepse_stock_symbol: str
    ltp: float
    date: datetime

class StockSource(str, Enum):
    IPO = "IPO"
    Secondary_Market = "Secondary Market"
    
class StorePortfolioData(BaseModel):
    stock_name: str
    total_shares: int
    purchase_rate: float
    total_purchase_value: float
    source: StockSource
    purchase_date: date
    
class PortfolioOut(StorePortfolioData):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class UpdatePortfolioData(BaseModel):
    stock_name: Optional[str] = None
    total_shares: Optional[int] = None
    purchase_rate: Optional[float] = None
    total_purchase_value: Optional[float] = None
    source: Optional[StockSource] = None
    purchase_date: Optional[date] = None