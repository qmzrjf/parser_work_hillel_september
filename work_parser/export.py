import csv
import json
import sqlite3

import settings


class ExportEngine:

    def __init__(self, json_mode: bool, db_mode: bool, csv_mode: bool):
        self.json_mode = json_mode
        self.db_mode = db_mode
        self.csv_mode = csv_mode

        if db_mode:
            self.__create_db()

    @staticmethod
    def __create_db():
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE vacancy (id integer, title text, link text)")
        conn.close()
        print("DB create successfully")

    def export(self, vacancies: list):
        if self.json_mode:
            with open(settings.JSON_PATH, "w") as file:
                json.dump([vacancy.to_dict() for vacancy in vacancies], file, indent=4, ensure_ascii=False)

        if self.csv_mode:
            csv_vacancies = [vacancy.to_dict() for vacancy in vacancies]
            keys = csv_vacancies[0].keys()
            with open(settings.CSV_PATH, "w") as file:
                writer = csv.DictWriter(file, keys)
                writer.writeheader()
                writer.writerows(csv_vacancies)

        if self.db_mode:
            conn = sqlite3.connect(settings.DB_PATH)
            cursor = conn.cursor()

            cursor.executemany("INSERT INTO vacancy VALUES (?,?,?)", [vacancy.to_list() for vacancy in vacancies])
            conn.commit()
            conn.close()
