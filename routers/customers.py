from fastapi import HTTPException, status, APIRouter
from models import Customer,CustomerCreate,CustomerUpdate
from db import SessionDep
from sqlmodel import select

routerCustomers = APIRouter()

@routerCustomers.post("/customers", response_model = Customer, tags=['Customers'])
async def create_costumer(customer_data: CustomerCreate, session: SessionDep):
    customerRegister = Customer.model_validate(customer_data.model_dump())
    session.add(customerRegister) #Crea la sentencia SQL
    session.commit() # Ejecuta la query
    session.refresh(customerRegister)
    return customerRegister

@routerCustomers.get("/customers", response_model = list[Customer], tags=['Customers'])
async def listCustomer(session: SessionDep):
    return session.exec(select(Customer)).all()

@routerCustomers.get("/customers/{id}", response_model=Customer, tags=['Customers'])
async def filterCustomer(id:int, session: SessionDep):
    customer = session.exec(select(Customer).where(Customer.id==id)).first()
    if customer != None:
        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail='El cliente no existe'
        )

@routerCustomers.delete("/customers/{id}", tags=['Customers'])
async def deleteCustomer(id:int, session:SessionDep):
    customer = session.exec(select(Customer).where(Customer.id==id)).first()
    if customer != None:
        session.delete(customer)
        session.commit()
        return {"detail":"ok"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail='El cliente no existe'
        )

@routerCustomers.patch("/customers/{id}",response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def updateCustomer(id:int, customer_data: CustomerUpdate ,session: SessionDep):
    customer = session.exec(select(Customer).where(Customer.id==id)).first()
    if customer != None:
        customer_data_dict = customer_data.model_dump(exclude_unset=True)
        customer.sqlmodel_update(customer_data_dict)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail='El cliente no existe'
        )