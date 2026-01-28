import sqlalchemy
from core.base import metadata

stats_table = sqlalchemy.Table(
    "stats",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("total_reviews", sqlalchemy.Integer),
    sqlalchemy.Column("positive_count", sqlalchemy.Integer),
    sqlalchemy.Column("negative_count", sqlalchemy.Integer),
    sqlalchemy.Column("positive_rate", sqlalchemy.Float),
    sqlalchemy.Column("trend_change", sqlalchemy.Float),
    sqlalchemy.Column("alert_count", sqlalchemy.Integer),
    sqlalchemy.Column("hot_topic_count", sqlalchemy.Integer),
    sqlalchemy.Column("top_topic", sqlalchemy.String(100)),
    sqlalchemy.Column("updated_at", sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),  # 自动更新时间
)