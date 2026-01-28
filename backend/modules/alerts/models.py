import sqlalchemy
from core.base import metadata

alerts_table = sqlalchemy.Table(
    "alerts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("type", sqlalchemy.String(50)),
    sqlalchemy.Column("severity", sqlalchemy.String(20)),
    sqlalchemy.Column("date", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("status", sqlalchemy.String(20)),
)