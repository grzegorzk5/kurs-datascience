import os, sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

root = os.getcwd()

if root not in sys.path:
    sys.path.insert(0, root)

# Ładowanie zmiennych z pliku .env
load_dotenv(dotenv_path=f"{root}/.env")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# Importowanie wszystkich baz metadanych
from models.articles import ArticleBase
from models.movies import MovieBase

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Mapowanie sekcji z alembic.ini do odpowiednich metadanych
metadata_map = {
    "articles_db": ArticleBase.metadata,
}

# Mapowanie sekcji z alembic.ini na nazwy zmiennych środowiskowych
env_mapping = {
    "articles_db": "ARTICLES_DB_URL",
}

# Sprawdzenie, która nazwa sekcji została użyta (np. "articles_db")
current_section = config.config_ini_section

target_metadata = metadata_map.get(current_section)

def get_url():
    """Pobiera URL z .env na podstawie aktualnej sekcji."""
    env_var_name = env_mapping.get(current_section)

    if env_var_name:
        url = os.getenv(env_var_name)
        if not url:
            raise ValueError(
                f"❌ Brak zmiennej {env_var_name} w pliku .env"
            )
        return url
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Pobranie parametrów sekcji (np. [articles_db])
    section_config = config.get_section(current_section, {})

    # Nadpisanie sqlalchemy.url wartością z .env
    section_config["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        section_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
