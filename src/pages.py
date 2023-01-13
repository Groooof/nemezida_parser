import typing as tp 

from lxml import html as _html


class BasePage:
    """
    Базовый класс для парсинга страниц.
    Принимает html в виде строки либо уже 
    подготовленного объекта lxml.html.HtmlElement
    """
    def __init__(self, html: tp.Union[str, _html.HtmlElement]) -> None:
        self.dom = html if isinstance(html, _html.HtmlElement) else _html.fromstring(html)
        self.xpath_begin = '.' if isinstance(html, _html.HtmlElement) else ''
            
    def find_element(self, xpath) -> str:
        """
        Поиск одного элемента под заданному выражению xpath.
        Если элементов несколько - возвращает первый из них.
        Если ничего не найдено - возвращает пустую строку
        """
        elems = self.find_elements(xpath)
        elem = ''.join(elems[:1])
        # return elem if elem else None
        return elem
    
    def find_elements(self, xpath) -> tp.List[str]:
        """
        Поиск нескольких элементов по заданному выражению xpath.
        Если ничего не найдено - возвращает пустой список.
        """
        return self.dom.xpath(self.xpath_begin + xpath)
    
    
class SearchPage(BasePage):
    """
    Парсинг страницы поиска с карточками.
    """
    def get_cards_links(self) -> tp.List[str]:
        xpath = '//h3/a/@href'
        res = self.find_elements(xpath)
        return res
    
    def get_pages_count(self) -> int:
        xpath = '//div[@class="nav-links"]/a[@class="page-numbers"][last()]/text()'
        res = self.find_element(xpath)
        if res:
            res = int(res)
        return res
    
    
class CardInfoItemPage(BasePage):
    """
    Парсинг строки доп. инфо. в карточке.
    """
    def get_name(self) -> str:
        xpath = '/b/text()'
        res = self.find_element(xpath)
        res = res.strip()
        return res
        
    def get_value(self) -> str:
        xpath = '/text()'
        res = self.find_element(xpath)
        res = res.strip()
        return res
    

class CardPage(BasePage):
    """
    Парсинг страницы карточки.
    """
    def get_fullname(self) -> str:
        xpath = '//h1[contains(@class, "post-title")]/a/text()'
        res = self.find_element(xpath)
        return res
    
    def get_date(self) -> str:
        xpath = '//span[@class="simple-grid-entry-meta-single-date"]/text()'
        res = self.find_element(xpath)
        res = res.strip()
        return res
    
    def get_category(self) -> str:
        xpath = '//a[contains(@rel, "category")]/text()'
        res = self.find_element(xpath)
        return res
    
    def get_photos_urls(self) -> tp.List[str]:
        xpath = '//div[@class="photos_single_place"]/a/@href'
        res = self.find_elements(xpath)
        return res
    
    def get_info(self) -> tp.Dict[str, str]:
        info = {}
        rows_xpath = '//div/b/..'
        
        rows = self.find_elements(rows_xpath)
        for row in rows:
            row_page = CardInfoItemPage(row)
            name = row_page.get_name()
            value = row_page.get_value()
            info[name] = value
        
        return info