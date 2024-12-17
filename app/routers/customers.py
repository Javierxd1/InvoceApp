from fastapi import HTTPException, status, APIRouter
from models import Customer,CustomerCreate, CustomerPlan,CustomerUpdate,Plan
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

@routerCustomers.post("/customers/{customer_id}/plans/{plan_id}",tags=['Customers'])
async def suscribe_customer(customer_id:int, plan_id:int, status: str, session:SessionDep):
    customer_db = session.get(Customer,customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el clinte o no existe el plan")
    
    customerPlan_db = CustomerPlan(plan_id=plan_db.id,customer_id=customer_db.id, status=status)
    session.add(customerPlan_db)
    session.commit()
    session.refresh(customerPlan_db)
    return customerPlan_db


@routerCustomers.get("/customers/{customer_id}/plans}",tags=['Customers'])
async def list_suscriptions_of_customer (customer_id:int, status_plan: str, session:SessionDep):
    customer_db = session.get(Customer,customer_id)

    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='El cliente no existe')
    
    return customer_db.plans


