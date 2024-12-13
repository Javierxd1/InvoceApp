from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship

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


class TransactionsBase(SQLModel):
    ammount: int
    description: str

class Transactions(TransactionsBase, table = True):
    id:int | None = Field(default=None, primary_key= True)
    customer_id: int = Field(foreign_key = "customer.id") #Crea la relación con la tabla Customer - aunque se define como customer
    customer:Customer = Relationship(back_populates="transactions")

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