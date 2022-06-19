import json


def get_all_posts(file_name: str) -> list[dict]:
    """Собирает все посты из базы данных"""
    with open(file_name, encoding='utf-8') as data_base:
        all_posts = json.load(data_base)
    return all_posts

def search_post_by_str(search_str: str, posts: list[dict]) -> list[dict]:
    """Сортирует предоставленные посты по вхождению строки"""
    posts_to_return = []
    for post in posts:
        if search_str in post['content']:
            posts_to_return.append(post)
    return posts_to_return
