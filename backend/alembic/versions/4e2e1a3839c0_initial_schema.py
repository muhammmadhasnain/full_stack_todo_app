# """initial schema

# Revision ID: 4e2e1a3839c0
# Revises: 
# Create Date: 2025-12-15 18:10:00.000000

# """
# from alembic import op
# import sqlalchemy as sa
# import sqlmodel


# revision identifiers
# revision = '4e2e1a3839c0'
# down_revision = None
# branch_labels = None
# depends_on = None


# def upgrade() -> None:
#     # Create user table
#     op.create_table('user',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#     sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#     sa.Column('created_at', sa.DateTime(), nullable=False),
#     sa.Column('updated_at', sa.DateTime(), nullable=False),
#     sa.Column('is_active', sa.Boolean(), nullable=False),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    
#     # Create recurrencepattern table
#     op.create_table('recurrencepattern',
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('pattern_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#     sa.Column('interval', sa.Integer(), nullable=False),
#     sa.Column('end_condition_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#     sa.Column('end_count', sa.Integer(), nullable=True),
#     sa.Column('end_date', sa.Date(), nullable=True),
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('created_at', sa.DateTime(), nullable=False),
#     sa.Column('updated_at', sa.DateTime(), nullable=False),
#     sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_recurrencepattern_user_id'), 'recurrencepattern', ['user_id'], unique=False)
    
#     # Create task table
#     op.create_table('task',
#     sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
#     sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
#     sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#     sa.Column('priority', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#     sa.Column('due_date', sa.DateTime(), nullable=True),
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('created_at', sa.DateTime(), nullable=False),
#     sa.Column('updated_at', sa.DateTime(), nullable=False),
#     sa.Column('completed_at', sa.DateTime(), nullable=True),
#     sa.Column('is_recurring', sa.Boolean(), nullable=False),
#     sa.Column('recurrence_pattern_id', sa.Integer(), nullable=True),
#     sa.ForeignKeyConstraint(['recurrence_pattern_id'], ['recurrencepattern.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_task_user_id'), 'task', ['user_id'], unique=False)
    
#     # Create tasktag table
#     op.create_table('tasktag',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('task_id', sa.Integer(), nullable=False),
#     sa.Column('tag_name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
#     sa.Column('created_at', sa.DateTime(), nullable=False),
#     sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_tasktag_task_id'), 'tasktag', ['task_id'], unique=False)


# def downgrade() -> None:
#     op.drop_index(op.f('ix_tasktag_task_id'), table_name='tasktag')
#     op.drop_table('tasktag')
#     op.drop_index(op.f('ix_task_user_id'), table_name='task')
#     op.drop_table('task')
#     op.drop_index(op.f('ix_recurrencepattern_user_id'), table_name='recurrencepattern')
#     op.drop_table('recurrencepattern')
#     op.drop_index(op.f('ix_user_email'), table_name='user')
#     op.drop_table('user')














"""Convert all integer IDs to UUID

Revision ID: 003_convert_all_ids_to_uuid
Revises: 4e2e1a3839c0
Create Date: 2025-12-16 17:40:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

revision = '003_convert_all_ids_to_uuid'
down_revision = '4e2e1a3839c0'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()

    # ---------------------
    # User Table
    # ---------------------
    op.add_column('user', sa.Column('_new_id', UUID(), nullable=True))
    users = conn.execute(sa.text("SELECT id FROM user")).fetchall()
    for u in users:
        conn.execute(
            sa.text("UPDATE user SET _new_id=:new_id WHERE id=:old_id"),
            {"new_id": str(uuid.uuid4()), "old_id": u[0]}
        )
    op.drop_constraint('user_pkey', 'user', type_='primary')
    op.drop_column('user', 'id')
    op.alter_column('user', '_new_id', new_column_name='id', nullable=False)
    op.create_primary_key('user_pkey', 'user', ['id'])

    # ---------------------
    # RecurrencePattern Table
    # ---------------------
    op.add_column('recurrencepattern', sa.Column('_new_id', UUID(), nullable=True))
    op.add_column('recurrencepattern', sa.Column('_new_user_id', UUID(), nullable=True))
    rp_rows = conn.execute(sa.text("SELECT id, user_id FROM recurrencepattern")).fetchall()
    for rp in rp_rows:
        old_id, old_user_id = rp
        new_id = str(uuid.uuid4())
        user_uuid = conn.execute(sa.text("SELECT id FROM user WHERE id=:uid"), {"uid": old_user_id}).fetchone()[0]
        conn.execute(
            sa.text("UPDATE recurrencepattern SET _new_id=:new_id, _new_user_id=:user_uuid WHERE id=:old_id"),
            {"new_id": new_id, "user_uuid": user_uuid, "old_id": old_id}
        )
    op.drop_constraint('recurrencepattern_pkey', 'recurrencepattern', type_='primary')
    op.drop_column('recurrencepattern', 'id')
    op.drop_column('recurrencepattern', 'user_id')
    op.alter_column('recurrencepattern', '_new_id', new_column_name='id', nullable=False)
    op.alter_column('recurrencepattern', '_new_user_id', new_column_name='user_id', nullable=False)
    op.create_primary_key('recurrencepattern_pkey', 'recurrencepattern', ['id'])
    op.create_foreign_key('recurrencepattern_user_id_fkey', 'recurrencepattern', 'user', ['user_id'], ['id'])

    # ---------------------
    # Task Table
    # ---------------------
    op.add_column('task', sa.Column('_new_id', UUID(), nullable=True))
    op.add_column('task', sa.Column('_new_user_id', UUID(), nullable=True))
    op.add_column('task', sa.Column('_new_recurrence_id', UUID(), nullable=True))
    task_rows = conn.execute(sa.text("SELECT id, user_id, recurrence_pattern_id FROM task")).fetchall()
    for t in task_rows:
        old_id, old_user_id, old_rp_id = t
        new_task_id = str(uuid.uuid4())
        user_uuid = conn.execute(sa.text("SELECT id FROM user WHERE id=:uid"), {"uid": old_user_id}).fetchone()[0]
        if old_rp_id:
            rp_uuid = conn.execute(sa.text("SELECT id FROM recurrencepattern WHERE id=:rid"), {"rid": old_rp_id}).fetchone()[0]
        else:
            rp_uuid = None
        conn.execute(
            sa.text("UPDATE task SET _new_id=:nid, _new_user_id=:uid, _new_recurrence_id=:rid WHERE id=:old_id"),
            {"nid": new_task_id, "uid": user_uuid, "rid": rp_uuid, "old_id": old_id}
        )
    op.drop_constraint('task_pkey', 'task', type_='primary')
    op.drop_constraint('task_user_id_fkey', 'task', type_='foreignkey')
    op.drop_constraint('task_recurrence_pattern_id_fkey', 'task', type_='foreignkey')
    op.drop_column('task', 'id')
    op.drop_column('task', 'user_id')
    op.drop_column('task', 'recurrence_pattern_id')
    op.alter_column('task', '_new_id', new_column_name='id', nullable=False)
    op.alter_column('task', '_new_user_id', new_column_name='user_id', nullable=False)
    op.alter_column('task', '_new_recurrence_id', new_column_name='recurrence_pattern_id', nullable=True)
    op.create_primary_key('task_pkey', 'task', ['id'])
    op.create_foreign_key('task_user_id_fkey', 'task', 'user', ['user_id'], ['id'])
    op.create_foreign_key('task_recurrence_pattern_id_fkey', 'task', 'recurrencepattern', ['recurrence_pattern_id'], ['id'])

    # ---------------------
    # TaskTag Table
    # ---------------------
    op.add_column('tasktag', sa.Column('_new_id', UUID(), nullable=True))
    op.add_column('tasktag', sa.Column('_new_task_id', UUID(), nullable=True))
    tt_rows = conn.execute(sa.text("SELECT id, task_id FROM tasktag")).fetchall()
    for tt in tt_rows:
        old_id, old_task_id = tt
        new_id = str(uuid.uuid4())
        task_uuid = conn.execute(sa.text("SELECT id FROM task WHERE id=:tid"), {"tid": old_task_id}).fetchone()[0]
        conn.execute(
            sa.text("UPDATE tasktag SET _new_id=:nid, _new_task_id=:tid WHERE id=:old_id"),
            {"nid": new_id, "tid": task_uuid, "old_id": old_id}
        )
    op.drop_constraint('tasktag_pkey', 'tasktag', type_='primary')
    op.drop_constraint('tasktag_task_id_fkey', 'tasktag', type_='foreignkey')
    op.drop_column('tasktag', 'id')
    op.drop_column('tasktag', 'task_id')
    op.alter_column('tasktag', '_new_id', new_column_name='id', nullable=False)
    op.alter_column('tasktag', '_new_task_id', new_column_name='task_id', nullable=False)
    op.create_primary_key('tasktag_pkey', 'tasktag', ['id'])
    op.create_foreign_key('tasktag_task_id_fkey', 'tasktag', 'task', ['task_id'], ['id'])

def downgrade():
    raise NotImplementedError("Downgrade not supported for full UUID migration")
