"""add oauth support to users

Revision ID: 001_oauth_support
Revises: 
Create Date: 2025-11-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_oauth_support'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add OAuth support fields to users table."""
    # Make password_hash nullable for OAuth users
    op.alter_column('users', 'password_hash',
                    existing_type=sa.String(255),
                    nullable=True)
    
    # Add OAuth fields
    op.add_column('users', sa.Column('auth_provider', sa.String(50), nullable=False, server_default='email'))
    op.add_column('users', sa.Column('oauth_provider_id', sa.String(255), nullable=True))
    
    # Add index for oauth_provider_id
    op.create_index('ix_users_oauth_provider_id', 'users', ['oauth_provider_id'])


def downgrade() -> None:
    """Remove OAuth support fields from users table."""
    # Drop index
    op.drop_index('ix_users_oauth_provider_id', table_name='users')
    
    # Drop OAuth columns
    op.drop_column('users', 'oauth_provider_id')
    op.drop_column('users', 'auth_provider')
    
    # Make password_hash not nullable again
    op.alter_column('users', 'password_hash',
                    existing_type=sa.String(255),
                    nullable=False)

