"""making valor_carga and valor_intercambio nullable

Revision ID: 26f388924d06
Revises: 968ffecb59af
Create Date: 2025-03-17 16:22:39.913706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26f388924d06'
down_revision: Union[str, None] = '968ffecb59af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('balanco_subsistema_horario', schema=None) as batch_op:
        batch_op.alter_column('valor_carga',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('valor_intercambio',
               existing_type=sa.FLOAT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('balanco_subsistema_horario', schema=None) as batch_op:
        batch_op.alter_column('valor_intercambio',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('valor_carga',
               existing_type=sa.FLOAT(),
               nullable=False)

    # ### end Alembic commands ###
