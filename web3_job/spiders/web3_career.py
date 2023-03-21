import json

import scrapy


class Web3CareerSpider(scrapy.Spider):
    name = "web3_career"
    allowed_domains = ["web3.career"]
    start_urls = ["http://web3.career/"]

    def parse(self, response):
        # print(response.text)
        post_xpath_list = response.xpath('//html/body/main/div/div/div/div/div/table/tbody[@class="tbody"]/tr')
        post_jd_xpath_list = response.xpath('//script[@type="application/ld+json"]')
        post_jd_list = []
        for row in post_jd_xpath_list:
            # print(row.root.text)
            json_data = json.loads(row.root.text)
            post_jd_list.append(json_data)
            print(json_data)
        for post_xpath_row in post_xpath_list:
            row = post_xpath_row.xpath('./td')
            post_name = post_xpath_row.xpath('./td/div/div/div/a/h2')[0].root.text
            company = post_xpath_row.xpath('./td/a/h3')[0].root.text
            post_time = post_xpath_row.xpath('./td/time').attrib['datetime']
            base_address_xpath = post_xpath_row.xpath('./td[@class="job-location-mobile"]/p')
            salary_xpath = post_xpath_row.xpath('./td/p[@title="Estimated salary based on similar jobs"]')

            if not salary_xpath:
                salary = None
            else:
                salary = salary_xpath[0].root.text
            base_address = ''
            if base_address_xpath:
                base_address = base_address_xpath[0].root.text
            else:
                base_address_xpath = post_xpath_row.xpath('./td[@class="job-location-mobile"][@style]')
                tem_xpath = base_address_xpath.xpath('./a[@style="font-size: 12px; color: #d5d3d3;"]')
                for base_address_row in tem_xpath:
                    base_address = "{base_address}, {other_base}".format(base_address=base_address,
                                                                         other_base=base_address_row.root.text)
                base_address = base_address[2:]

            # print(base_address)
            print(post_name, company, post_time, base_address, salary)


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl web3_career".split()
    cmdline.execute(args)
