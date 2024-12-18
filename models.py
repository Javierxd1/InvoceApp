from enum import Enum
from pydantic import BaseModel,EmailStr, field_validator
from sqlalchemy import Select
from sqlmodel import SQLModel,Field,Relationship,Session
from db import engine

class statusEnum(str,Enum): #Permite definir los valores pretederminados del Status
    Active ='Activo'
    Inactive = 'Inactivo'


class CustomerPlan(SQLModel,table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id : int = Field(foreign_key="customer.id")
    status: statusEnum = Field(default=statusEnum.Active) #La clase Enum permite elegir valores puntuales
    

class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list['Customer'] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description : str | None = Field(default=None)
    email : EmailStr = Field(default=None) # Se añande el EmailStr, para validar la insersión de mails.
    age : int = Field(default=None)

    #Se crear un validador contra la base de datos del email ingresado.
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        session = Session(engine) #Se deben importar desde db y desde SQLmodel
        query = Select(Customer).where(Customer.email == value)
        result = session.exec(query).first()

        if result != None:
            raise ValueError('Este Email ya está registrado')
        return value

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table = True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transactions"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates='customers', link_model=CustomerPlan
    )


class TransactionsBase(SQLModel):
    ammount: int
    description: str

class Transactions(TransactionsBase, table = True):
    id:int | None = Field(default=None, primary_key= True)
    customer_id: int = Field(foreign_key = "customer.id") #Crea la relación con la tabla Customer - aunque se define como customer
    customer: Customer = Relationship(back_populates="transactions")

class TransactionsCreate(TransactionsBase):
    customer_id: int = Field(foreign_key = "customer.id")

class Invoice(BaseModel):
    id:int
    customer: Customer
    transactions : list[Transactions]
    total:int

    @property
    def totalAmmount(self):
        return sum(self.transactions.ammount for transaction in self.transactions)