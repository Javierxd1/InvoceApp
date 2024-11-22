from fastapi import HTTPException, status, APIRouter
from models import Transactions
from db import SessionDep
from sqlmodel import select

routerTransactions = APIRouter()

@routerTransactions.post("/transactions", tags=['Transactions'])
async def create_costumer(transactions_data: Transactions):
    return transactions_data