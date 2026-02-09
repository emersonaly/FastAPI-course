from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..models import Transaction, TransactionCreate, TransactionUpdate, Customer
from ..db import SessionDep

router = APIRouter(tags=["transactions"])

@router.post("/transactions", response_model=Transaction)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dic = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dic.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    
    transaction_db = Transaction.model_validate(transaction_data_dic)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get("/transactions", response_model=list[Transaction])
async def list_transaction(session: SessionDep):
    return session.exec(select(Transaction)).all()

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def read_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction doesn't exits"
        )
    return transaction_db

@router.patch("/transactions/{transaction_id}", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def update_transaction(transaction_id: int, transaction_data: TransactionUpdate, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction doesn't exits"
        )
    transaction_data_dic = transaction_data.model_dump(exclude_unset=True)
    transaction_db.sqlmodel_update(transaction_data_dic)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction doesn't exits"
        )
    session.delete(transaction_db)
    session.commit()
    return {"detail": "ok"}