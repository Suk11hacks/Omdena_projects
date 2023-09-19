from urllib.parse import urljoin

import scrapy
from bs4 import BeautifulSoup

# from scrapy.loader.processors import MapCompose, Join
from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader

from wikiSpider.items import NewsArticleItem


class DainikNepalgunjSpider(scrapy.Spider):
    name = "dainiknepalgunj_spider"
    allowed_domains = ["www.dainiknepalgunj.com", "dainiknepalgunj.com", "dainiknepalgunj"]
    # Starting with a single category.
    # We changes this url as we move on to next category.
    start_urls = ["https://dainiknepalgunj.com/category/%E0%A4%A8%E0%A5%8D%E0%A4%AF%E0%A5%82%E0%A4%9C%E0%A4%97%E0%A4%A8%E0%A5%8D%E0%A4%9C"]


    def parse(self, response):
        # Get all the article urls
        all_article_urls = (
            response.xpath(
                "//div[@class='grid-box mix1']/div[@class='col-md-12 col-xs-12 pps m-b-1']/a/@href"
            ).extract()
        )

        for article_url in all_article_urls:
            absolute_url = urljoin(response.url, article_url)

            yield scrapy.Request(absolute_url, callback=self.parse_article)

        # Get the next index URLs and yield Requests
        next_selector = response.xpath(f'//div[@class="flex justify-between flex-1 sm:hidden"]/a[contains(text(), "Next")]/@href')
        print("------------------")
        print(next_selector.extract_first())
        # next_selector = response.xpath(
        #     "//a[contains(@class, 'next page-numbers')]/@href"
        # )
        # print(next_selector)
        # print("nextse")
        if next_selector:
            absolute_url = urljoin(response.url, next_selector.extract_first())
            yield scrapy.Request(absolute_url, callback=self.parse)

    def parse_article(self, response):
        news_url = response.url
        try:
            title = (
                response.xpath("//div[@class='container']/div[@class='col-md-9 col-xs-12']/h1/text()")
                .extract_first()
                .strip()
            )
            author = (
                response.xpath("//div[@class='author-name']/p[@class='author m-0']/text()")
                .extract_first()
                .strip()
            )
            content = response.xpath("//div[@class='description']/p/text()")
            if not content:
                content = response.xpath("//div[@class='description']//p/text()")
            content = content.extract()
            published_date = (
                response.xpath("//div[@class='author-name']/p[@class='news-time m-0']/text()")
                .extract_first()
                # .strip()
            )
            category = "NewsGunj"
        except Exception as e:
            title = "Error"
            content = "Error"
            published_date = "Error"
            author = "Error"
            category = "Error"




        l = ItemLoader(item=NewsArticleItem(), response=response)
        l.add_value("title", title)
        # l.add_value("content", content)
        l.add_value(
            "content",
            content,
            MapCompose(lambda x: BeautifulSoup(x, "html.parser").get_text()),
        )
        l.add_value("published_date", published_date)
        l.add_value("news_url", news_url)
        l.add_value("author", author)
        l.add_value("Category", category)

        class NewsArticleItem(Item):
        # Primary fields
        title = Field()
        content = Field()
        author = Field()
        # cover_image_url = Field()
        published_date = Field()
        # tags = Field()
        news_url = Field()
        Category = Field()

        # l.add_value("url", response.url)
        # l.add_value("project", self.settings.get("BOT_NAME"))
        # l.add_value("spider", self.name)
        # l.add_value("server", socket.gethostname())
        # l.add_value("date", datetime.datetime.now())

        return l.load_item()
