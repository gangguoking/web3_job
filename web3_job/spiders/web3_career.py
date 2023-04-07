import json
import logging

import scrapy


MAX_PAGE = 2


class Web3CareerSpider(scrapy.Spider):
    name = "web3_career"
    allowed_domains = ["web3.career"]
    start_urls = ["https://web3.career/"]

    def parse(self, response):
        post_career_xpath_list = response.xpath('///table[@class="table table-borderless"]/tbody[@class="tbody"]/tr')
        job_dict = {}
        for row in post_career_xpath_list:
            job_id = row.xpath('./td[1]/div/div/div/a[@style=" text-decoration: none"]').attrib['href']
            job_name = row.xpath('./td[1]/div/div/div/a[@style=" text-decoration: none"]/h2')[0].root.text[:-1]
            job_dict[job_name] = job_id

        post_jd_xpath_list = response.xpath('//script[@type="application/ld+json"]')
        for row in post_jd_xpath_list:
            try:
                json_data = json.loads(row.root.text)
            except Exception as exc:
                logging.warning(exc)
                continue
            if json_data['@type'] == 'JobPosting':
                yield json_data

        if response.url == "https://web3.career/":
            next_url = "https://web3.career/?page={page}".format(page="2")
        else:
            page = response.url.split('page=')[-1]
            if int(page) > MAX_PAGE - 1:
                return
            next_url = "https://web3.career/?page={page}".format(page=str(int(page) + 1))

        yield scrapy.Request(url=next_url,
                             dont_filter=True,
                             callback=self.parse)


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl web3_career".split()
    cmdline.execute(args)
