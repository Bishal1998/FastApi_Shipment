"""initial

Revision ID: 4b94f8668064
Revises:
Create Date: 2026-04-28 21:06:15.221432

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "4b94f8668064"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "sellers",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("zip_code", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "delivery_partners",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "serviceable_zipcodes", postgresql.ARRAY(sa.Integer()), nullable=True
        ),
        sa.Column("max_handling_capacity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tags",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "name",
            sa.Enum(
                "EXPRESS",
                "STANDARD",
                "FRAGILE",
                "HEAVY",
                "INTERNATIONAL",
                "DOMESTIC",
                "TEMPERATYURE_CONTROLLED",
                "GIFT",
                "RETURN",
                "DOCUMENTS",
                name="tagname",
            ),
            nullable=False,
        ),
        sa.Column("instruction", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "shipments",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("address", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("destination", sa.Integer(), nullable=False),
        sa.Column("estimated_delivery", sa.TIMESTAMP(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("client_contact_email", sa.String(), nullable=False),
        sa.Column("client_contact_phone", sa.String(), nullable=False),
        sa.Column("seller_id", postgresql.UUID(), nullable=False),
        sa.Column("delivery_partner_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["seller_id"], ["sellers.id"]),
        sa.ForeignKeyConstraint(["delivery_partner_id"], ["delivery_partners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "shipment_tags",
        sa.Column("shipment_id", postgresql.UUID(), nullable=False),
        sa.Column("tag_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["shipment_id"], ["shipments.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"]),
        sa.PrimaryKeyConstraint("shipment_id", "tag_id"),
    )

    op.create_table(
        "shipment_event",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("location", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PLACED",
                "IN_TRANSIT",
                "DELIVERED",
                "OUT_FOR_DELIVERY",
                name="shipmentstatus",
            ),
            nullable=False,
        ),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("shipment_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["shipment_id"], ["shipments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reviews",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("shipment_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["shipment_id"], ["shipments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Seed tags
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
    op.drop_table("reviews")
    op.drop_table("shipment_event")
    op.drop_table("shipment_tags")
    op.drop_table("shipments")
    op.drop_table("tags")
    op.drop_table("delivery_partners")
    op.drop_table("sellers")
    op.execute("DROP TYPE shipmentstatus")
    op.execute("DROP TYPE tagname")
