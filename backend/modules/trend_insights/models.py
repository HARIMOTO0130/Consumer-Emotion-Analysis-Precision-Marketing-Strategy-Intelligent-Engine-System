import sqlalchemy
from core.base import metadata

trend_insights_table = sqlalchemy.Table(
    "trend_insights",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("text", sqlalchemy.Text),
)