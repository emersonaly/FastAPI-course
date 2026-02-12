from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select

from ..models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum
from ..db import SessionDep

router = APIRouter()
# asi aplica para todos los endpoints router = APIRouter(tags = ['customers'])


@router.post("/customers", response_model=Customer, tags=["customers"], status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    return customer_db

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    customer_data_dic = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dic)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.post("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, 
                                    plan_status: StatusEnum = Query()
                                    ):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer or plan doesn't exits"
        )
    customer_plan = CustomerPlan(customer_id=customer_db.id, plan_id=plan_db.id, active=plan_status)
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan

@router.get("/customers/{customer_id}/plans", tags=["customers"])
async def subscribe_customer_plans(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    # customer_plans = session.exec(
    #     select(CustomerPlan).where(
    #         CustomerPlan.customer_id == customer_id, 
    #         CustomerPlan.active == True
    #     )
    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.active == plan_status)
    )
    customer_plans = session.exec(query).all()
    return customer_plans
