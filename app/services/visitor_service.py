from sqlalchemy.orm import Session
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate


def create_visitor(db: Session, data: VisitorCreate) -> Visitor:
    visitor = Visitor(
        name=data.name,
        mobile=data.mobile
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor


def get_all_visitors(db: Session):
    return db.query(Visitor).order_by(Visitor.visited_at.desc()).all()


def get_visitor_by_id(db: Session, visitor_id: int):
    return db.query(Visitor).filter(Visitor.id == visitor_id).first()


def update_visitor(db: Session, visitor_id: int, data: VisitorCreate) -> Visitor:
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if visitor:
        visitor.name = data.name
        visitor.mobile = data.mobile
        db.commit()
        db.refresh(visitor)
    return visitor


def delete_visitor(db: Session, visitor_id: int):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if visitor:
        db.delete(visitor)
        db.commit()
        return True
    return False
