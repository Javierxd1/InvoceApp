from fastapi import APIRouter
from models import Plan
from db import SessionDep
from sqlmodel import select


routerPlans = APIRouter()

@routerPlans.post('/plans', tags=['Plans'])
async def create_plan(plan_data:Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@routerPlans.get('/Plans', response_model=list[Plan],tags=['Plans'])
def list_plan(session:SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans


