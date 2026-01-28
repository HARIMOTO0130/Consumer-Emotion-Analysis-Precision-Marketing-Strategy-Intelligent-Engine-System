import random

class CommentCrawler:
    """这里放爬虫等工具函数"""
    @staticmethod
    def clean_text(text: str):
        return text.strip().replace("\n", "")