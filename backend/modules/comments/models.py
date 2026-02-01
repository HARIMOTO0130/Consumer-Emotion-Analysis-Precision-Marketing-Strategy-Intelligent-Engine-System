import sqlalchemy
from core.base import metadata

comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("text", sqlalchemy.Text),
    sqlalchemy.Column("source", sqlalchemy.String(50)),
    sqlalchemy.Column("time", sqlalchemy.String(10)),
    sqlalchemy.Column("emotion", sqlalchemy.String(20)),
    sqlalchemy.Column("sentiment", sqlalchemy.String(20)),
    sqlalchemy.Column("intensity", sqlalchemy.String(10)),
    sqlalchemy.Column("timestamp", sqlalchemy.String(20)),
)