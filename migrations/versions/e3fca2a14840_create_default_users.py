"""create default users

Revision ID: e3fca2a14840
Revises: 4c1b34a46bbe
Create Date: 2025-09-06 00:45:30.632325

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from app.config.Auth import hash_password


# revision identifiers, used by Alembic.
revision: str = 'e3fca2a14840'
down_revision: Union[str, Sequence[str], None] = '4c1b34a46bbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Criar usuário admin padrão
    admin_id = str(uuid.uuid4())
    basic_id = str(uuid.uuid4())
    admin_password = hash_password("admin_magalu")
    basic_password = hash_password("basic_magalu")

    op.execute(
        f"""
        INSERT INTO clients (id, name, email, password, role)
        VALUES ('{admin_id}', 'Administrador Magazine', 'admin_magazine@gmail.com', '{admin_password}', 1)
        """
    )

    op.execute(
        f"""
        INSERT INTO clients (id, name, email, password, role)
        VALUES ('{basic_id}', 'Básico Magazine', 'basico_magazine@gmail.com', '{basic_password}', 2)
        """
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        f"""
        DELETE FROM clients where email='admin_magazine@gmail.com'
        """
    )

    op.execute(
        f"""
        DELETE FROM clients where email='basico_magazine@gmail.com'
        """
    )
    pass
