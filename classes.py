import json
import os.path
from datetime import datetime
import flask
from globals import UPLOAD_FOLDER
import logging

class EmptyPostError(Exception):
    pass
class DecodingError(Exception):
    pass

class DataBase:
    """Класс работает с базой данных (сбор, поиск, добавление)"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_data = self.get_db_data()

    def get_db_data(self) -> list[dict]:
        """Загружает и возвращает базу"""
        try:
            with open(self.db_path, encoding='utf-8') as db_file:
                file_content = json.load(db_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.db_path} не найден")
            return
        except json.decoder.JSONDecodeError:
            raise DecodingError(f'Не удалось преобразовать {self.db_path}')
            return

        return file_content

    def search_str_in_db_data(self, search_line):
        """Ищет в базе данных совпадающие посты и возвращает их списком"""
        logging.info(f'Был произведен поиск. Запрос: - {search_line}')

        to_return = []
        for item in self.db_data:
            if search_line.lower() in item['content'].lower():
                to_return.append(item)
        return to_return

    def append_new_post_to_db(self, new_post_info):
        """добавляет пост в базу данных"""
        self.db_data.append(new_post_info)
        with open(self.db_path, 'w', encoding='utf-8') as db_file:
            json.dump(self.db_data, db_file, ensure_ascii=False, indent=4)

class NewPostFromRequestData:
    """Класс работает с новым постом (формирует, проверяет, отдает информацию для экспорта в виде словаря, сохраняет файл"""
    def __init__(self, request_data: flask.Request):
        self.picture = request_data.files.get('picture')
        self.picture_name = self.picture.filename
        self.extension = self.picture.content_type.split('/')[-1]
        self.content = request_data.values.get('content')

        self.pic_full_path = self.generate_file_name()

        self.validate_post()

    def generate_file_name(self):
        """Генерирует путь с именем  файла для сохранения (для уникализации имён)"""

        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_name = f"{current_time}_{self.picture_name}"
        full_path = os.path.join(UPLOAD_FOLDER, file_name)

        return full_path

    def validate_post(self):
        """Проверяет на расширение файла и на соджержимое сообщения поста"""
        if self.extension not in ['jpeg', 'png']:
            logging.info(f'Была произведена попытка загрузить файл с расширением {self.extension}')
            raise TypeError("Error: only .jpeg and .png are available.")

        if len(self.content) == 0:
            logging.info(f'Была произведена попытка загрузить файл с пустым комментарием')
            raise EmptyPostError('Error: no empty posts is available.')



    def get_info_to_export(self):
        """возвращает подходящий для экспорта словарь"""
        info_to_export = {

            'pic': '\\' + self.pic_full_path,
            # 'pic': self.pic_full_path,
            'content': self.content
        }

        return info_to_export

    def save_file(self):
        """Сохраняет фотографию"""
        try:
            self.picture.save(self.pic_full_path)
        except BaseException as e:
            logging.error(f"Ошибка при загрузке файла")
            raise e


