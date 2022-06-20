from flask import render_template, Blueprint, request
from main.functions import get_all_posts, search_post_by_str

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='./templates', static_folder='/static')

@main_blueprint.route('/')
def main_page():
    return render_template('index.html')


@main_blueprint.route('/search')
def search_page():
    search_line = request.args['s']
    all_posts = get_all_posts('posts.json')

    if not all_posts:
        return "Ошибка считывания"

    sorted_posts = search_post_by_str(search_line, all_posts)
    return render_template('searched_posts.html', search_line=search_line, posts=sorted_posts)