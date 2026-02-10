from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..models import Plan
from ..db import SessionDep

router = APIRouter(tags=["plans"])

@router.get("/plans")
async def get_plans(session: SessionDep):
    return session.exec(select(Plan)).all()

@router.post("/plans")
async def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

