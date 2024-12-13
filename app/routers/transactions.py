from fastapi import HTTPException, status, APIRouter
from models import Transactions,TransactionsCreate,Customer
from db import SessionDep
from sqlmodel import select

routerTransactions = APIRouter()

@routerTransactions.post("/createTransactions", tags=['Transactions'])
async def create_transaction(transactions_data: TransactionsCreate, session:SessionDep):
    transactions_data_dict = transactions_data.model_dump() #Convierte en diccionario los datos de transacción de entrada
    customer = session.get(Customer, transactions_data_dict.get('customer_id')) #Busca el id del customer dentro de la base Customer

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El cliente no existe')
    
    transaction_db = Transactions.model_validate(transactions_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@routerTransactions.get("/transactions", tags=['Transactions'])
async def list_transaction(session:SessionDep):
    query = select(Transactions)
    transactions = session.exec(query).all()
    return transactions