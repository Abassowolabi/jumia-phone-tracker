from scrapy import Spider
from scrapy.http import Request

class PhoneSpiderSpider(Spider):
    name = "phone_spider"
    allowed_domains = ["www.jumia.com.ng"]
    start_urls = ["https://www.jumia.com.ng/mobile-phones/"]
     
    # each product's URL
    def parse(self, response):
        page_count = response.meta.get('page_count', 1)

        phones_links = response.xpath('//a[@class="core"]/@href').getall()[:15]
        for urls in phones_links:
            absolute_urls = response.urljoin(urls)
            yield Request(absolute_urls,
                          callback=self.parse_page,
                          meta={'product_url': absolute_urls})
        
        # pagination for just 4 pages
        if page_count < 4:
            next_page_url = response.xpath('//*[@class="pg _act"]/following-sibling::a/@href').get()
            if next_page_url:
                absolute_next_page_url = response.urljoin(next_page_url)
                yield Request(absolute_next_page_url,
                              callback=self.parse,
                              meta={'page_count': page_count + 1})

        else:
            self.logger.info(f"Stopped pagination after {page_count} pages.")

    # extracting more data
    def parse_page(self, response):

        # Extracting product details with error handling for missing values
        
        title = response.xpath('//title/text()').get()
        title = title.split('|')[0].strip() if title else 'No title found'
        
        price = response.xpath('//*[contains(@class, "-fs24") and contains(@class, "-b")]/text()').get()
        price = price.strip() if price else 'Price not available'
        
        rating = response.xpath(
            '//*[contains(@class, "stars") and contains(@class, "_m") and contains(@class, "_al")]/text()').get()
        rating = rating.strip() if rating else 'No rating'
        
        availability = response.xpath('//p[contains(text(), "units left")]/text()').get()
        availability = availability.strip() if availability else 'Availability unknown'

        yield {
            'links': response.meta['product_url'],
            'titles': title,
            'prices': price,
            'ratings': rating,
            'availability': availability
        }





