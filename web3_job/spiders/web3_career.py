import json

import scrapy


MAX_PAGE = 7

COMPANY_LIST = {
  "Kodex": "james@kodex.io",
  "GammaSwap Labs": "dgoodkin@gammaswap.com",
  "Lemon.io": "https://lemon.io/escape-the-matrix/",
  "Etherscan": "jobs@etherscan.io"
}


class Web3CareerSpider(scrapy.Spider):
    name = "web3_career"
    allowed_domains = ["web3.career"]
    start_urls = ["https://web3.career/"]

    def parse(self, response):
        post_jd_xpath_list = response.xpath('//script[@type="application/ld+json"]')
        if "post_jd_list" in response.meta:
            post_jd_list = response.meta['post_jd_list']
        else:
            post_jd_list = []
        for row in post_jd_xpath_list:
            json_data = json.loads(row.root.text)
            if json_data['@type'] == 'JobPosting':
                company_name = json_data['hiringOrganization']['name']
                if company_name in COMPANY_LIST:
                    # print(json_data['hiringOrganization']['name'])
                    json_data['apply'] = COMPANY_LIST[company_name]
                else:
                    continue
                print(json_data)
                post_jd_list.append(json_data)
            # yield json_data

        with open('data.json', 'w', encoding='utf-8') as fp:
            json.dump({'post_jd_list': post_jd_list}, fp)

        if response.url == "https://web3.career/":
            next_url = "https://web3.career/?page={page}".format(page="2")
        else:
            page = response.url.split('page=')[-1]
            if int(page) > MAX_PAGE - 1:
                return
            next_url = "https://web3.career/?page={page}".format(page=str(int(page) + 1))

        yield scrapy.Request(url=next_url,
                             dont_filter=True,
                             callback=self.parse,
                             meta={"post_jd_list": post_jd_list})


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl web3_career".split()
    cmdline.execute(args)
