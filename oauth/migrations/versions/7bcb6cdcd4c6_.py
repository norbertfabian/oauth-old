"""empty message

Revision ID: 7bcb6cdcd4c6
Revises: None
Create Date: 2016-06-22 00:00:57.546087

"""

# revision identifiers, used by Alembic.
revision = '7bcb6cdcd4c6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id_contact', sa.Integer(), server_default=sa.text(u"nextval('contact_seq')"), nullable=False),
    sa.Column('company', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('www', sa.String(length=100), nullable=True),
    sa.Column('gsm', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('custom_id', sa.String(length=20), nullable=True),
    sa.Column('ic', sa.String(length=20), nullable=True),
    sa.Column('dic', sa.String(length=20), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('zip', sa.String(length=10), nullable=True),
    sa.Column('bank_account', sa.String(length=50), nullable=True),
    sa.Column('bank_code', sa.String(length=50), nullable=True),
    sa.Column('iban', sa.String(length=50), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('hash', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id_contact'),
    sa.UniqueConstraint('hash')
    )
    op.create_table('client',
    sa.Column('id_client', sa.Integer(), server_default=sa.text(u"nextval('client_seq')"), nullable=False),
    sa.Column('id_contact', sa.Integer(), nullable=True),
    sa.Column('display', sa.String(length=50), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('gid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_contact'], ['contact.id_contact'], ),
    sa.PrimaryKeyConstraint('id_client'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('user',
    sa.Column('id_user', sa.Integer(), server_default=sa.text(u"nextval('user_seq')"), nullable=False),
    sa.Column('id_contact', sa.Integer(), nullable=True),
    sa.Column('is_device', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('is_superadmin', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('validation_type', sa.Integer(), nullable=True),
    sa.Column('registered', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['id_contact'], ['contact.id_contact'], ),
    sa.PrimaryKeyConstraint('id_user')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('application',
    sa.Column('id_application', sa.Integer(), server_default=sa.text(u"nextval('application_seq')"), nullable=False),
    sa.Column('oauth', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('id_client', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('token', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('active', sa.Boolean(), server_default='true', nullable=True),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.Column('return_path', sa.String(length=200), nullable=True),
    sa.Column('conf', sa.String(), nullable=True),
    sa.Column('calc_user', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('payment', sa.Integer(), server_default='0', nullable=True),
    sa.Column('period', sa.Integer(), server_default='0', nullable=True),
    sa.Column('alive', sa.Integer(), nullable=True),
    sa.Column('restore', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_client'], ['client.id_client'], ),
    sa.PrimaryKeyConstraint('id_application'),
    sa.UniqueConstraint('token')
    )
    op.create_table('domain',
    sa.Column('id_domain', sa.Integer(), server_default=sa.text(u"nextval('domain_seq')"), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('id_client', sa.Integer(), nullable=True),
    sa.Column('validated', sa.Boolean(), server_default='false', nullable=True),
    sa.ForeignKeyConstraint(['id_client'], ['client.id_client'], ),
    sa.PrimaryKeyConstraint('id_domain'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_domain_id_client'), 'domain', ['id_client'], unique=False)
    op.create_table('user_client',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_client', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['id_client'], ['client.id_client'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_client')
    )
    op.create_table('validation',
    sa.Column('id_validation', sa.Integer(), server_default=sa.text(u"nextval('validation_seq')"), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('secret', sa.String(length=10), nullable=True),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.Column('use', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_validation')
    )
    op.create_index(op.f('ix_validation_id_user'), 'validation', ['id_user'], unique=False)
    op.create_index(op.f('ix_validation_secret'), 'validation', ['secret'], unique=False)
    op.create_table('application_contact',
    sa.Column('id_application', sa.Integer(), nullable=False),
    sa.Column('id_contact', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_application'], ['application.id_application'], ),
    sa.ForeignKeyConstraint(['id_contact'], ['contact.id_contact'], ),
    sa.PrimaryKeyConstraint('id_application', 'id_contact')
    )
    op.create_table('application_user',
    sa.Column('id_application', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_contact', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('is_staff', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=True),
    sa.ForeignKeyConstraint(['id_application'], ['application.id_application'], ),
    sa.ForeignKeyConstraint(['id_contact'], ['contact.id_contact'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_application', 'id_user')
    )
    op.create_table('application_user_contact',
    sa.Column('id_application', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_contact', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_application'], ['application.id_application'], ),
    sa.ForeignKeyConstraint(['id_contact'], ['contact.id_contact'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_application', 'id_user', 'id_contact')
    )
    op.create_table('token',
    sa.Column('id_token', sa.Integer(), server_default=sa.text(u"nextval('token_seq')"), nullable=False),
    sa.Column('id_application', sa.Integer(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('validated', sa.Boolean(), nullable=True),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('last_activity', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_application'], ['application.id_application'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_token'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_token_id_application'), 'token', ['id_application'], unique=False)
    op.create_index(op.f('ix_token_id_user'), 'token', ['id_user'], unique=False)
    op.create_table('user_domain',
    sa.Column('id', sa.Integer(), server_default=sa.text(u"nextval('user_domain_seq')"), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_domain', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('accepted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_domain'], ['domain.id_domain'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_domain_id_domain'), 'user_domain', ['id_domain'], unique=False)
    op.create_index(op.f('ix_user_domain_id_user'), 'user_domain', ['id_user'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_domain_id_user'), table_name='user_domain')
    op.drop_index(op.f('ix_user_domain_id_domain'), table_name='user_domain')
    op.drop_table('user_domain')
    op.drop_index(op.f('ix_token_id_user'), table_name='token')
    op.drop_index(op.f('ix_token_id_application'), table_name='token')
    op.drop_table('token')
    op.drop_table('application_user_contact')
    op.drop_table('application_user')
    op.drop_table('application_contact')
    op.drop_index(op.f('ix_validation_secret'), table_name='validation')
    op.drop_index(op.f('ix_validation_id_user'), table_name='validation')
    op.drop_table('validation')
    op.drop_table('user_client')
    op.drop_index(op.f('ix_domain_id_client'), table_name='domain')
    op.drop_table('domain')
    op.drop_table('application')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('client')
    op.drop_table('contact')
    ### end Alembic commands ###
