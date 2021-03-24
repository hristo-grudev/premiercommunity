import scrapy

from scrapy.loader import ItemLoader

from ..items import PremiercommunityItem
from itemloaders.processors import TakeFirst


class PremiercommunitySpider(scrapy.Spider):
	name = 'premiercommunity'
	start_urls = ['https://www.premiercommunity.com/bank-news.html']

	def parse(self, response):
		post_links = response.xpath('//p[@class="read-more"]/a[@property="url"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//main[@id="content"]//text()[normalize-space() and not(ancestor::h1 | ancestor::p[@class="date-category"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=PremiercommunityItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
