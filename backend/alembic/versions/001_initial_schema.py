"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-04-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.Column("oauth_provider", sa.String(50), nullable=True),
        sa.Column("oauth_id", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("notification_enabled", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("notification_time", sa.Time(), server_default=sa.text("'08:00:00'")),
        sa.UniqueConstraint("oauth_provider", "oauth_id", name="unique_oauth"),
    )
    op.create_index("idx_users_email", "users", ["email"])
    op.create_index("idx_users_oauth", "users", ["oauth_provider", "oauth_id"])

    op.create_table(
        "chapters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("sanskrit_name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("shloka_count", sa.Integer(), nullable=False),
        sa.CheckConstraint("id BETWEEN 1 AND 18", name="check_chapter_id"),
    )

    op.create_table(
        "shlokas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("chapter", sa.Integer(), sa.ForeignKey("chapters.id"), nullable=False),
        sa.Column("shloka_number", sa.Integer(), nullable=False),
        sa.Column("sanskrit_text", sa.Text(), nullable=False),
        sa.Column("transliteration", sa.Text(), nullable=False),
        sa.Column("meaning", sa.Text(), nullable=False),
        sa.Column("audio_file_path", sa.String(500), nullable=True),
        sa.Column("themes", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("embedding_index", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.UniqueConstraint("chapter", "shloka_number", name="unique_shloka"),
    )
    op.create_index("idx_shlokas_chapter", "shlokas", ["chapter"])

    op.create_table(
        "bookmarks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chapter", sa.Integer(), nullable=False),
        sa.Column("shloka_number", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "chapter", "shloka_number", name="unique_user_bookmark"),
    )
    op.create_index("idx_bookmarks_user", "bookmarks", ["user_id"])

    op.create_table(
        "reading_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chapter", sa.Integer(), nullable=False),
        sa.Column("shloka_number", sa.Integer(), nullable=False),
        sa.Column("last_read_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "chapter", "shloka_number", name="unique_user_progress"),
    )
    op.create_index("idx_progress_user", "reading_progress", ["user_id"])

    op.create_table(
        "daily_wisdom",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("date", sa.Date(), unique=True, nullable=False),
        sa.Column("chapter", sa.Integer(), nullable=False),
        sa.Column("shloka_number", sa.Integer(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_daily_wisdom_date", "daily_wisdom", ["date"])


def downgrade() -> None:
    op.drop_table("daily_wisdom")
    op.drop_table("reading_progress")
    op.drop_table("bookmarks")
    op.drop_table("shlokas")
    op.drop_table("chapters")
    op.drop_table("users")
