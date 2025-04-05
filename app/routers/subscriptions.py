# routers/subscriptions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils, database
from datetime import datetime

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

@router.get("/", response_model=list[schemas.Subscription])
def get_user_subscriptions(
    current_user: models.User = Depends(utils.get_current_user),
    db: Session = Depends(database.get_db)
):
    return db.query(models.Subscription).filter(models.Subscription.user_id == current_user.id).all()

@router.post("/", response_model=schemas.Subscription)
def create_subscription(
    subscription: schemas.SubscriptionCreate,
    current_user: models.User = Depends(utils.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Deactivate existing subscriptions
    active_subscriptions = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id,
        models.Subscription.is_active == True
    ).all()
    
    for sub in active_subscriptions:
        sub.is_active = False
    
    # Create new subscription
    db_subscription = models.Subscription(
        user_id=current_user.id,
        plan_type=subscription.plan_type,
        end_date=subscription.end_date
    )
    
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    
    return db_subscription

@router.get("/active", response_model=schemas.Subscription)
def get_active_subscription(
    current_user: models.User = Depends(utils.get_current_user),
    db: Session = Depends(database.get_db)
):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id,
        models.Subscription.is_active == True,
        models.Subscription.end_date > datetime.utcnow()
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    return subscription