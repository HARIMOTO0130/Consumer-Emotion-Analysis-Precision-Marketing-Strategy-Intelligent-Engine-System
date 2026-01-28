import sqlalchemy
from core.base import metadata

emotion_distribution_table = sqlalchemy.Table(
    "emotion_distribution",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("channel", sqlalchemy.String(50)),
    sqlalchemy.Column("positive", sqlalchemy.Integer),
    sqlalchemy.Column("negative", sqlalchemy.Integer),
    sqlalchemy.Column("positive_percent", sqlalchemy.Float),
)