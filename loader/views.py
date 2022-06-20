from flask import render_template, Blueprint, request
from loader.functions import formate_post, append_post_to_db

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='./templates', static_folder='/static')

@loader_blueprint.route('/', methods=["GET"])
def main_page():
    return render_template('post_form.html')


@loader_blueprint.route('/load', methods=["POST"])
def load():
    #формирование поста и сохранение файла
    try:
        formated_post = formate_post(request)
    except TypeError:
        return "Неверный формат файла. Загрузите jpeg или png"

    #добавление информации в бд
    result = append_post_to_db(formated_post, 'posts.json')

    if not result:
        return "Ошибка загрузки"
    return render_template('post_uploaded.html', post=formated_post)
