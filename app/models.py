from app.db import engine
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select
from app.db import engine


class StatusEnum(str, Enum):
    ACTIVE = True
    INACTIVE = False

class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    active: StatusEnum = Field(default=StatusEnum.ACTIVE)


class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates="plans",
        link_model=CustomerPlan
        )


class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        customer = session.exec(query).first()
        if customer:
            raise ValueError("This email already exists")
        return value


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(
        back_populates="customers",
        link_model=CustomerPlan
        )
    # invoices: List["Invoice"] = Relationship(back_populates="customer")


class TransactionBase(SQLModel):
    # id: int
    ammount: int
    description: str

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")


class TransactionUpdate(TransactionBase):
    pass

    
class InvoiceBase(SQLModel):
    id: int
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    pass


class Invoice(InvoiceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # customer_id: int | None = Field(default=None, foreign_key="customer.id")
    # customer: Customer = Relationship(back_populates="invoices")
    # transactions: List[Transaction] = Relationship(back_populates="invoice")
