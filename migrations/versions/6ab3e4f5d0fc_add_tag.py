"""add tag

Revision ID: 6ab3e4f5d0fc
Revises: 789272c11eb4
Create Date: 2026-05-09 13:14:02.328548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ab3e4f5d0fc'
down_revision: Union[str, Sequence[str], None] = '789272c11eb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('shipments', 'client_contact_email',
               existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('shipments', 'client_contact_phone',
               existing_type=sa.VARCHAR(), nullable=True)
    op.add_column('tags', sa.Column('name', sa.Enum('EXPRESS', 'STANDARD', 'FRAGILE', 'HEAVY', 'INTERNATIONAL', 'DOMESTIC', 'TEMPERATYURE_CONTROLLED', 'GIFT', 'RETURN', 'DOCUMENTS', name='tagname'), nullable=False))
    op.add_column('tags', sa.Column('instruction', sa.String(), nullable=False))

    op.execute("""
    INSERT INTO tags (id, name, instruction) VALUES
    (gen_random_uuid(), 'EXPRESS', ''),
    (gen_random_uuid(), 'STANDARD', ''),
    (gen_random_uuid(), 'FRAGILE', 'Handle with care'),
    (gen_random_uuid(), 'HEAVY', ''),
    (gen_random_uuid(), 'INTERNATIONAL', ''),
    (gen_random_uuid(), 'DOMESTIC', ''),
    (gen_random_uuid(), 'TEMPERATYURE_CONTROLLED', 'Keep refrigerated'),
    (gen_random_uuid(), 'GIFT', ''),
    (gen_random_uuid(), 'RETURN', ''),
    (gen_random_uuid(), 'DOCUMENTS', '')
""")


def downgrade() -> None:
    op.drop_column('tags', 'instruction')
    op.drop_column('tags', 'name')
    op.alter_column('shipments', 'client_contact_phone',
               existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('shipments', 'client_contact_email',
               existing_type=sa.VARCHAR(), nullable=True)