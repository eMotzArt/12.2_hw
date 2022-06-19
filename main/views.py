from flask import render_template, Blueprint

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def main_page():
    return "Это страничка сообщений"

#
# @main_blueprint.route('/inbox')
# def inbox_page():
#     return "Это страничка входящих сообщений"
