from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..models import Invoice, InvoiceCreate, InvoiceUpdate
from ..db import SessionDep

router = APIRouter(tags=["invoices"])

@router.post("/invoices", response_model=Invoice)
async def create_invoice(invoice_data: InvoiceCreate, session: SessionDep):
    invoice = Invoice.model_validate(invoice_data.model_dump())
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice

@router.get("/invoices", response_model=list[Invoice])
async def list_invoice(session: SessionDep):
    return session.exec(select(Invoice)).all()

@router.get("/invoices/{invoice_id}", response_model=Invoice)
async def read_invoice(invoice_id: int, session: SessionDep):
    invoice_db = session.get(Invoice, invoice_id)
    if not invoice_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice doesn't exits"
        )
    return invoice_db

@router.patch("/invoices/{invoice_id}", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, session: SessionDep):
    invoice_db = session.get(Invoice, invoice_id)
    if not invoice_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice doesn't exits"
        )
    invoice_data_dic = invoice_data.model_dump(exclude_unset=True)
    invoice_db.sqlmodel_update(invoice_data_dic)
    session.add(invoice_db)
    session.commit()
    session.refresh(invoice_db)
    return invoice_db

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int, session: SessionDep):
    invoice_db = session.get(Invoice, invoice_id)
    if not invoice_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice doesn't exits"
        )
    session.delete(invoice_db)
    session.commit()
    return {"detail": "ok"}