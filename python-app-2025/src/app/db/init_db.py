from app.db.session import engine
from app.db import models


def create_tables() -> None:
    """Create DB tables. For development only; for production use migrations (alembic)."""
    models.Base = models.Base if hasattr(models, 'Base') else None
    # Import Base from session to ensure single declarative base
    from app.db.session import Base

    Base.metadata.create_all(bind=engine)
