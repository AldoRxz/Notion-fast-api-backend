"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-11
"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # extensions (safe attempts)
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS citext;')

    # enums
    role_name = sa.Enum('owner','admin','editor','commenter','viewer', name='role_name')
    page_type = sa.Enum('page','database', name='page_type')
    role_name.create(op.get_bind(), checkfirst=True)
    page_type.create(op.get_bind(), checkfirst=True)

    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('email', postgresql.CITEXT(), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('workspaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False, unique=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('workspace_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', role_name, nullable=False, server_default='editor'),
        sa.UniqueConstraint('workspace_id','user_id', name='uq_workspace_user')
    )

    op.create_table('pages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('parent_page_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('pages.id', ondelete='SET NULL')),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('type', page_type, nullable=False, server_default='page'),
        sa.Column('icon', sa.String()),
        sa.Column('cover_url', sa.String()),
        sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('page_content',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('page_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('pages.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
    )

    op.create_index('ix_pages_workspace_parent', 'pages', ['workspace_id','parent_page_id'])


def downgrade() -> None:
    op.drop_index('ix_pages_workspace_parent', table_name='pages')
    op.drop_table('page_content')
    op.drop_table('pages')
    op.drop_table('workspace_members')
    op.drop_table('workspaces')
    op.drop_table('users')
    sa.Enum(name='page_type').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='role_name').drop(op.get_bind(), checkfirst=True)
    
