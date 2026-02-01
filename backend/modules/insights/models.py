import sqlalchemy
from core.base import metadata

insights_table = sqlalchemy.Table(
    "insights",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("type", sqlalchemy.String(50)),
    sqlalchemy.Column("date", sqlalchemy.String(20)),
    sqlalchemy.Column("text", sqlalchemy.Text),
    sqlalchemy.Column("action", sqlalchemy.String(100)),
    sqlalchemy.Column("action_text", sqlalchemy.String(100)),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("recommendation", sqlalchemy.Text),
    sqlalchemy.Column("priority", sqlalchemy.String(10)),
    sqlalchemy.Column("expected_outcome", sqlalchemy.Text),
)