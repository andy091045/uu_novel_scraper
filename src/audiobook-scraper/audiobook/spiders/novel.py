import scrapy
from scrapy_playwright.page import PageMethod
from .utils.text_processor import TextProcessor
from pathlib import Path


class NovelSpider(scrapy.Spider):
    name = "novel"
    start_urls_section_selector = "#list-chapterAll a::attr(href)"
    sub_urls_section_selector = ".readcotent"
    output_dir = "novels/"

    def __init__(self, start_url=None, **kwargs):
        super().__init__(start_url, **kwargs)
        self.start_url = start_url
        self.urls = set()
        self.text_processor = TextProcessor()

    async def start(self):
        yield scrapy.Request(
            url=self.start_url,
            callback=self.get_all_urls,
            meta={
                "playwright": True,
            },
        )

    def get_all_urls(self, response):
        title = response.css("title::text").get()
        self.output_dir = Path(self.output_dir) / title.strip()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        urls = response.css(self.start_urls_section_selector).getall()

        self.urls = [
            response.urljoin(url)
            for url in urls
        ]

        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                },
            )

    def parse(self, response):
        title = response.css("title::text").get()
        content = response.css(
            self.sub_urls_section_selector + " ::text"
        ).getall()

        result = self.text_processor.clean(content)

        self.text_processor.export_txt(
            self.output_dir,
            title,
            result
        )
