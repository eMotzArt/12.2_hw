import json
from datetime import datetime
from json import JSONDecodeError

import flask

def formate_post(request_data: flask.Request):

    # забираем картинку
    picture = request_data.files.get('picture')
    if picture.content_type not in ['image/jpeg', 'image/png']:
        raise TypeError("Допустимы расширения только .jpeg или .png")
        return




    #формируем путь и имя для файла
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    pic_path = f'uploads/images/{current_time}_{picture.filename}'

    #сохраняем картинку
    picture.save(pic_path)

    # текст
    post_text = request_data.values.get('content')

    # словарь для добавления в базу
    to_db_info = {
        'pic': pic_path,
        'content': post_text
    }
    return to_db_info

def append_post_to_db(post, file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as data_base:
            all_posts: list[dict] = json.load(data_base)
    except FileNotFoundError:
        print("Файл не найден")
        return
    except JSONDecodeError:
        print("Файл не удается преобразовать")
        return

    all_posts.append(post)

    with open(file_name, 'w', encoding='utf-8') as data_base:
        json.dump(all_posts, data_base, ensure_ascii=False, indent=4)

    return True
