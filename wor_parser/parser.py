from bs4 import BeautifulSoup, Tag


class ParserEngine:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @staticmethod
    def find_id_and_href(card: Tag) -> tuple[str, str]:
        tag_a = card.find("h2").find("a")
        href = tag_a["href"]
        vacancy_id = href.strip("/").split("/")[-1]
        return href, vacancy_id

    def find_cards(self, class_: str) -> list[Tag]:
        cards = self.soup.find_all("div", class_=class_)
        extended_class = class_ + " mt-lg"
        first_card = self.soup.find_all("div", class_=extended_class)
        return cards + first_card

    def get_title(self) -> str:
        h1 = self.soup.find("h1", class_="my-0")
        title = h1.text
        return title
