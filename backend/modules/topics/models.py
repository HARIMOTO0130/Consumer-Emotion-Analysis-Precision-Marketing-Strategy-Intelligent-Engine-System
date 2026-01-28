import sqlalchemy
from core.base import metadata

topics_table = sqlalchemy.Table(
    "topics",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("rank", sqlalchemy.Integer),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("mentions", sqlalchemy.Integer),
    sqlalchemy.Column("sentiment", sqlalchemy.String(20)),
    sqlalchemy.Column("trend", sqlalchemy.String(20)),
)