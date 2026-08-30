from sqlalchemy.orm import Session

from app.models.audit_log import AuditAction, AuditLog


def log_action(
    db: Session,
    user_id: int | None,
    action: AuditAction,
    resource_type: str | None = None,
    resource_id: int | None = None,
    ip_address: str | None = None,
) -> None:
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
    )
    db.add(entry)
    db.commit()
