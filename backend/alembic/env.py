import os
import sys
from logging.config import fileConfig
from sqlmodel import SQLModel
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Add the project root to the Python path so imports work
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Import your models here to register them with SQLModel
from src.models.user import User
from src.models.task import Task
from src.models.task_tag import TaskTag
from src.models.recurrence import RecurrencePattern

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = SQLModel.metadata

# Set database URL from environment
config.set_main_option('sqlalchemy.url', os.getenv('NEON_DATABASE_URL', ''))

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()