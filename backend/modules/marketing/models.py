import sqlalchemy
from core.base import metadata

marketing_activities_table = sqlalchemy.Table(
    "marketing_activities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(255)),
    sqlalchemy.Column("participants", sqlalchemy.Integer),
    sqlalchemy.Column("effect", sqlalchemy.String(20)),
    sqlalchemy.Column("engagement", sqlalchemy.Float),
    sqlalchemy.Column("conversion", sqlalchemy.Float),
    sqlalchemy.Column("date", sqlalchemy.String(20)),
    sqlalchemy.Column("priority", sqlalchemy.String(20)),
)