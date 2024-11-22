from fastapi import HTTPException, status, APIRouter
from models import Invoice
from db import SessionDep
from sqlmodel import select

routerInvoices = APIRouter()

@routerInvoices.post("/invoice", tags=['Invoices'])
async def create_costumer(invoice_data: Invoice):
    return invoice_data 