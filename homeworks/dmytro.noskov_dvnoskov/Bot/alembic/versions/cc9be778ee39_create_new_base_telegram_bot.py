"""create new base telegram_bot

Revision ID: cc9be778ee39
Revises: 
Create Date: 2017-03-25 20:56:55.426029

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = 'cc9be778ee39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('buy',
                    sa.Column('buy_id', sa.Integer, primary_key=True),
                    sa.Column('username', sa.String(15)),
                    sa.Column('phone', sa.String(20)),
                    sa.Column('data_city', sa.String(20)),
                    sa.Column('data_time', sa.String(20)),
                    sa.Column('city', sa.String(125)),
                    sa.Column('menu', sa.String(25)),
                    sa.Column('price', sa.Integer()),
                    sa.Column('calendar', sa.String(10)),
                    sa.Column('created_on', sa.DateTime(), default=datetime.now),
                    )

    op.create_table('users',
                    sa.Column('user_id', sa.Integer, primary_key=True),
                    sa.Column('username', sa.String(15)),
                    sa.Column('email_address', sa.String(255)),
                    sa.Column('phone', sa.String(20)),
                    sa.Column('token', sa.String(25)),
                    sa.Column('created_on', sa.DateTime(), default=datetime),
                    sa.Column('updated_on', sa.DateTime(), default=datetime, onupdate=datetime),
                    )

def downgrade():
    op.drop_table('buy')
    op.drop_table('users')
    pass

