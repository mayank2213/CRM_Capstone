from __future__ import annotations

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class AuditMixin:
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    updated_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)


class User(db.Model, AuditMixin):
    __tablename__ = "users"

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="Sales Rep")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self) -> bool:  # pragma: no cover - Flask-Login contract
        return True

    @property
    def is_anonymous(self) -> bool:  # pragma: no cover - Flask-Login contract
        return False

    def get_id(self) -> str:
        return str(self.id)


class Company(db.Model, AuditMixin):
    __tablename__ = "companies"

    name = db.Column(db.String(255), nullable=False, index=True)
    industry = db.Column(db.String(120))
    website = db.Column(db.String(255))
    notes = db.Column(db.Text)

    contacts = db.relationship("Contact", back_populates="company", lazy="selectin")
    deals = db.relationship("Deal", back_populates="company", lazy="selectin")


class Contact(db.Model, AuditMixin):
    __tablename__ = "contacts"

    name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), index=True)
    phone = db.Column(db.String(50))
    title = db.Column(db.String(120))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    company = db.relationship("Company", back_populates="contacts")
    deals = db.relationship("Deal", back_populates="contact", lazy="selectin")


class PipelineStage(db.Model, AuditMixin):
    __tablename__ = "pipeline_stages"

    name = db.Column(db.String(120), nullable=False, unique=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_default = db.Column(db.Boolean, nullable=False, default=False)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)


class Deal(db.Model, AuditMixin):
    __tablename__ = "deals"

    title = db.Column(db.String(255), nullable=False, index=True)
    value = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey("pipeline_stages.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    company = db.relationship("Company", back_populates="deals")
    contact = db.relationship("Contact", back_populates="deals")
    stage = db.relationship("PipelineStage")
    owner = db.relationship("User", foreign_keys=[owner_id])
    stage_history = db.relationship(
        "DealStageHistory",
        back_populates="deal",
        order_by="DealStageHistory.changed_at.asc()",
        lazy="selectin",
    )
    activities = db.relationship(
        "Activity",
        back_populates="deal",
        order_by="Activity.created_at.desc()",
        lazy="selectin",
    )


class DealStageHistory(db.Model):
    __tablename__ = "deal_stage_history"

    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"), nullable=False)
    from_stage_id = db.Column(db.Integer, db.ForeignKey("pipeline_stages.id"))
    to_stage_id = db.Column(db.Integer, db.ForeignKey("pipeline_stages.id"), nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    changed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    deal = db.relationship("Deal", back_populates="stage_history")
    from_stage = db.relationship("PipelineStage", foreign_keys=[from_stage_id], lazy="joined")
    to_stage = db.relationship("PipelineStage", foreign_keys=[to_stage_id], lazy="joined")
    changed_by = db.relationship("User", foreign_keys=[changed_by_id], lazy="joined")


class Activity(db.Model, AuditMixin):
    __tablename__ = "activities"

    activity_type = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"), nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    deal = db.relationship("Deal", back_populates="activities")
    contact = db.relationship("Contact", lazy="joined")
    author = db.relationship("User", foreign_keys=[author_id], lazy="joined")


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(120), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False, index=True)
    action = db.Column(db.String(120), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id], lazy="joined")


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    if not user_id:
        return None
    return db.session.get(User, int(user_id))
