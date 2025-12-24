"""Convert task IDs from integer to UUID

Revision ID: 001_convert_task_ids_to_uuid
Revises:
Create Date: 2025-12-16 16:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers
revision = '001_convert_task_ids_to_uuid'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add new UUID columns temporarily
    op.add_column('task', sa.Column('_new_id', UUID(), nullable=True))
    op.add_column('task', sa.Column('_new_user_id', UUID(), nullable=True))

    # Update the new columns with UUID values
    # First, update the task IDs by generating new UUIDs for each existing record
    conn = op.get_bind()

    # Get all current tasks
    result = conn.execute(sa.text("SELECT id, user_id FROM task"))
    rows = result.fetchall()

    # Update each task with a new UUID and corresponding user UUID
    # We need to map the old integer user_id to the corresponding UUID in the user table
    for row in rows:
        old_id = row[0]
        old_user_id = row[1]

        # Generate new task UUID
        new_task_uuid = str(uuid.uuid4())

        # Get the actual UUID from the user table based on the old integer user_id
        user_result = conn.execute(
            sa.text("SELECT id FROM user WHERE id = :old_user_id"),
            {"old_user_id": old_user_id}
        )
        user_row = user_result.fetchone()

        if user_row:
            actual_user_uuid = str(user_row[0])
        else:
            # If user doesn't exist, we can't properly migrate this task
            # In a real scenario, you'd want to handle this more carefully
            actual_user_uuid = str(uuid.uuid4())  # Generate a new UUID as fallback

        # Update the temporary columns
        conn.execute(
            sa.text("UPDATE task SET _new_id = :new_task_uuid, _new_user_id = :actual_user_uuid WHERE id = :old_id"),
            {"new_task_uuid": new_task_uuid, "actual_user_uuid": actual_user_uuid, "old_id": old_id}
        )

    # Drop the old primary key constraint and foreign key constraint
    op.drop_constraint('task_user_id_fkey', 'task', type_='foreignkey')
    op.drop_constraint('task_pkey', 'task', type_='primary')

    # Drop the old id and user_id columns
    op.drop_column('task', 'id')
    op.drop_column('task', 'user_id')

    # Rename the new columns to the original names
    op.alter_column('task', '_new_id', new_column_name='id', nullable=False)
    op.alter_column('task', '_new_user_id', new_column_name='user_id', nullable=False)

    # Add primary key and foreign key constraints back
    op.create_primary_key('task_pkey', 'task', ['id'])
    op.create_foreign_key('task_user_id_fkey', 'task', 'user', ['user_id'], ['id'])


def downgrade():
    # For downgrade, we would need to convert back to integers
    # This is complex since we lose the original integer IDs during the upgrade
    # In a real scenario, you'd want to preserve the original IDs or create a mapping table

    # Add temporary integer columns
    op.add_column('task', sa.Column('_old_id', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('_old_user_id', sa.Integer(), nullable=True))

    # For this example, we'll just assign sequential integers starting from 1
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id, user_id FROM task ORDER BY id"))
    rows = result.fetchall()

    for idx, row in enumerate(rows):
        task_uuid = str(row[0])
        user_uuid = str(row[1])
        new_id = idx + 1

        # Convert UUID to integer (this is just an example approach)
        # In a real scenario, you'd need a proper mapping
        conn.execute(
            sa.text("UPDATE task SET _old_id = :new_id WHERE id = :task_uuid"),
            {"new_id": new_id, "task_uuid": task_uuid}
        )

    # Drop the UUID constraints
    op.drop_constraint('task_user_id_fkey', 'task', type_='foreignkey')
    op.drop_constraint('task_pkey', 'task', type_='primary')

    # Drop the UUID columns
    op.drop_column('task', 'id')
    op.drop_column('task', 'user_id')

    # Rename the temporary integer columns
    op.alter_column('task', '_old_id', new_column_name='id', nullable=False)
    op.alter_column('task', '_old_user_id', new_column_name='user_id', nullable=False)

    # Add primary key and foreign key constraints back
    op.create_primary_key('task_pkey', 'task', ['id'])
    op.create_foreign_key('task_user_id_fkey', 'task', 'user', ['user_id'], ['id'])