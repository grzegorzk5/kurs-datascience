from alembic import context

import os, sys

root = os.getcwd()

if root not in sys.path:
    sys.path.insert(0, root)

from migrations.common_env import run_migrations_online, run_migrations_offline

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
