from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship

class CustomerPlan(SQLModel,table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id : int = Field(foreign_key="customer.id")
    status: str = Field(default=None)
    

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
    email : EmailStr = Field(default=None)
    age : int = Field(default=None)

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