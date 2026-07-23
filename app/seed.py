from decimal import Decimal

from sqlalchemy import inspect

from .extensions import db
from .models import Company, Contact, Deal, PipelineStage, User


def seed_demo_data():
    if not inspect(db.engine).has_table("users"):
        db.create_all()

    if User.query.first():
        return

    admin = User(name="Admin User", email="admin@example.com", role="Manager")
    admin.set_password("password123")
    db.session.add(admin)

    stages = [
        PipelineStage(name="New", sort_order=1, is_default=True),
        PipelineStage(name="Contacted", sort_order=2),
        PipelineStage(name="Qualified", sort_order=3),
        PipelineStage(name="Proposal", sort_order=4),
        PipelineStage(name="Won", sort_order=5, is_closed=True),
        PipelineStage(name="Lost", sort_order=6, is_closed=True),
    ]
    db.session.add_all(stages)
    db.session.flush()

    company = Company(
        name="RPATech",
        industry="Automation",
        website="https://example.com",
        notes="Demo account",
        created_by_id=admin.id,
        updated_by_id=admin.id,
    )
    contact = Contact(
        name="Aarav Sharma",
        email="aarav@example.com",
        phone="+91 90000 00000",
        title="Sales Head",
        company=company,
        created_by_id=admin.id,
        updated_by_id=admin.id,
    )
    deal = Deal(
        title="Automation Expansion",
        value=Decimal("125000.00"),
        company=company,
        contact=contact,
        stage=stages[0],
        owner_id=admin.id,
        created_by_id=admin.id,
        updated_by_id=admin.id,
    )

    db.session.add_all([company, contact, deal])
    db.session.commit()
