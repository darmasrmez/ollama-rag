from pathlib import Path
import scrapy

class ESCOMspider(scrapy.Spider):
    name = "escom"

    def start_requests(self):
        start_urls = [
            'https://www.escom.ipn.mx/',
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Get all the links of the page to access them and download the HTML
        # of each one
        links = response.css('a::attr(href)').getall()
        visited = set()
        for link in links:
            # I don't wnna download the same page again so I check if the link
            # is already in the path, also if the link ends with .gob.mx I don't
            # want to download it
            if not link.endswith('.gob.mx') and link not in visited:
                visited.add(link)
                yield response.follow(url=link, callback=self.parse_page)

    def parse_page(self, response):
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        with open(f'../data/{filename}', 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')