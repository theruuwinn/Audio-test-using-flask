
from alembic import op
import sqlalchemy as sa



revision = '0f29465a7773'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table('audiobook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uploaded_time', sa.DateTime(), nullable=False),
    sa.Column('duration_time', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('narrator', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('podcast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uploaded_time', sa.DateTime(), nullable=False),
    sa.Column('duration_time', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('host', sa.String(length=100), nullable=False),
    sa.Column('participents', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uploaded_time', sa.DateTime(), nullable=False),
    sa.Column('duration_time', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
  


def downgrade():
    
    op.drop_table('song')
    op.drop_table('podcast')
    op.drop_table('audiobook')
   
