from fastapi import FastAPI, Depends, HTTPException, Path
from schemas import GetStockPrice, StorePortfolioData, UserCreate, UserOut, Token, PortfolioOut, UpdatePortfolioData  
from datetime import datetime
from stock_scrapper import get_ltp
from models import User, Portfolio
from auth import hash_password, authenticate_user, create_access_token, get_current_user
from tortoise.contrib.fastapi import register_tortoise
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

app = FastAPI()

@app.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    hashed_pw = hash_password(user.password)
    user_obj = await User.create(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    return user_obj


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/store_portfolio_data", response_model=PortfolioOut, description="Store portfolio data for the logged-in user")
async def store_portfolio_data(
    data: StorePortfolioData,
    user: User = Depends(get_current_user)
):
    existing = await Portfolio.filter(
        user=user,
        stock_name=data.stock_name,
        purchase_date=data.purchase_date,
        purchase_rate=data.purchase_rate
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Portfolio already exists for this stock on this date with the same purchase rate. You may edit it instead."
        )

    portfolio = await Portfolio.create(
        user=user,
        stock_name=data.stock_name,
        total_shares=data.total_shares,
        purchase_rate=data.purchase_rate,
        total_purchase_value=data.total_purchase_value,
        source=data.source,
        purchase_date=data.purchase_date
    )
    return portfolio


@app.get("/get_portfolio_data", response_model=List[PortfolioOut], description="Get all portfolio entries for the logged-in user")
async def get_portfolio_data(user: User = Depends(get_current_user)):
    portfolio_items = await Portfolio.filter(user=user).all()
    return portfolio_items


@app.patch("/edit_portfolio_data/{portfolio_id}", response_model=PortfolioOut, description="Partially update a portfolio entry")
async def patch_portfolio_data(
    portfolio_id: int,
    data: UpdatePortfolioData,
    user: User = Depends(get_current_user)
):
    portfolio = await Portfolio.get_or_none(id=portfolio_id, user=user)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio entry not found")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(portfolio, field, value)
    
    await portfolio.save()
    return portfolio


@app.delete("/delete_portfolio_data/{portfolio_id}", description="Delete a portfolio entry")
async def delete_portfolio_data(
    portfolio_id: int = Path(..., description="ID of the portfolio entry to delete"),
    user: User = Depends(get_current_user)
):
    portfolio = await Portfolio.get_or_none(id=portfolio_id, user=user)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio entry not found")
    
    await portfolio.delete()
    return {"detail": f"Portfolio entry {portfolio_id} deleted successfully"}


@app.get("/get_stock_price/{symbol}", response_model=GetStockPrice)
async def get_stock_price(symbol: str, user: User = Depends(get_current_user)):
    ltp = get_ltp(symbol)
    if ltp is None:
        raise ValueError(f"Could not fetch LTP for stock symbol: {symbol}")
    return GetStockPrice(nepse_stock_symbol=symbol, ltp=ltp, date=datetime.now())


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/me", response_model=UserOut, description="Get currently logged-in user's info")
async def get_me(user: User = Depends(get_current_user)):
    return user


# Register DB
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
