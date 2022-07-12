from flask import render_template, Blueprint, request
from classes import DataBase, NewPostFromRequestData
from globals import POSTS_FILE

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='./templates', static_folder='/static')

@loader_blueprint.route('/', methods=["GET"])
def main_page():
    return render_template('post_form.html')


@loader_blueprint.route('/', methods=["POST"])
def load():
    try:
        #создаем объект с данными
        new_post = NewPostFromRequestData(request)
    except BaseException as e:
        return f"{e}"

    #получаем инфу для экспорта в базу данных
    to_export = new_post.get_info_to_export()

    try:
        #открываем базу
        current_db = DataBase(POSTS_FILE)
    except BaseException as e:
        return f'Ошибка: "{e}"'

    #закидываем в базу данные
    current_db.append_new_post_to_db(to_export)

    try:
        #сохраняем файл
        new_post.save_file()
    except BaseException as e:
        return f'Ошибка: "{e}"'

    #выводим новый пост
    return render_template('post_uploaded.html', post=to_export)
