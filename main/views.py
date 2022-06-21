from flask import render_template, Blueprint, request, abort
from classes import DataBase
from globals import POSTS_FILE

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='./templates', static_folder='/static')

@main_blueprint.route('/')
def main_page():
    return render_template('index.html')


@main_blueprint.route('/search')
def search_page():
    search_line = request.args['s']
    try:
        db = DataBase(POSTS_FILE)
    except BaseException as e:
        return f'Ошибка: "{e}"'

    search_result = db.search_str_in_db_data(search_line)

    return render_template('searched_posts.html', search_line=search_line, posts=search_result)
