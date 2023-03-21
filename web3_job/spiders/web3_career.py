import json

import scrapy


class Web3CareerSpider(scrapy.Spider):
    name = "web3_career"
    allowed_domains = ["web3.career"]
    start_urls = ["http://web3.career/"]

    def parse(self, response):
        post_jd_xpath_list = response.xpath('//script[@type="application/ld+json"]')
        post_jd_list = []
        for row in post_jd_xpath_list:
            json_data = json.loads(row.root.text)
            post_jd_list.append(json_data)
            yield json_data


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl web3_career".split()
    cmdline.execute(args)
