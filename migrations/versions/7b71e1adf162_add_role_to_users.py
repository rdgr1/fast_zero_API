"""add role to users

Revision ID: 7b71e1adf162
Revises: 97f48ea08bfc
Create Date: 2025-06-23 17:38:42.336495

"""
from alembic import op
import sqlalchemy as sa


# revisione estes valores conforme seu env.py
revision = "7b71e1adf162"  
# troque <sua_última_revision> pelo hash do arquivo anterior:
down_revision = "28d4d94cae37"  
branch_labels = None  
depends_on = None  


def upgrade():
    # 1) criar o tipo ENUM no Postgres (serve checkfirst=True pra não dar erro se já existir)
    role_enum = sa.Enum("STUDENT", "TEACHER", "ADMIN", name="roleenum")
    role_enum.create(op.get_bind(), checkfirst=True)

    # 2) adicionar a coluna role na tabela users, com default STUDENT em todos registros existentes
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("STUDENT", "TEACHER", "ADMIN", name="roleenum"),
            nullable=False,
            server_default="STUDENT",
        ),
    )
    # opcional: remover o server_default depois, se você não quiser manter default no schema
    op.alter_column("users", "role", server_default=None)


def downgrade():
    # 1) remover a coluna
    op.drop_column("users", "role")
    # 2) dropar o tipo
    sa.Enum(name="roleenum").drop(op.get_bind(), checkfirst=True)