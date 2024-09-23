import argparse
import os
import shutil

from bs4 import BeautifulSoup

import settings
from work_parser import ExportEngine, ParserEngine, RequestEngine, Vacancy


def create_data_directory():
    path = os.path.join(settings.PARENT_DIR, "data")

    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    os.makedirs(path)


def main(json_mode: bool, db_mode: bool, csv_mode: bool):
    create_data_directory()
    page = settings.START_PAGE
    result = []
    request_engine = RequestEngine()
    export_engine = ExportEngine(json_mode, db_mode, csv_mode)

    while True:
        print(f"PAGE {page}")

        response = request_engine.get_response(settings.HOST + settings.ROOT_PATH, {
            "ss": settings.SS,
            "page": page
        })

        parser_engine = ParserEngine(BeautifulSoup(response.text, "html.parser"))
        cards = parser_engine.find_cards("card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block")

        for card in cards:
            vacancy = Vacancy()
            href, vacancy_id = parser_engine.find_id_and_href(card)
            vacancy.vacancy_id = int(vacancy_id)
            vacancy_url = settings.HOST + href
            vacancy.href = vacancy_url
            print(vacancy_url)

            response = request_engine.get_response(vacancy_url)
            parser_engine.soup = BeautifulSoup(response.text, "html.parser")
            title = parser_engine.get_title()
            vacancy.title = title
            result.append(vacancy)

        if result:
            export_engine.export(result)

        if not cards:
            break

        page += 1
        result = []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser for work ua")
    parser.add_argument("-json", action="store_true", default=False, help="JSON store opportunity")
    parser.add_argument("-db", action="store_true", default=False, help="DB store opportunity")
    parser.add_argument("-csv", action="store_true", default=False, help="CSV store opportunity")
    args = parser.parse_args()
    main(args.json, args.db, args.csv)
