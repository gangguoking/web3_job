import json
import logging

import scrapy

MAX_PAGE = 40


COMPANY_DICT = {
  "Kodex": "james@kodex.io",
  "GammaSwap Labs": "dgoodkin@gammaswap.com",
  "Lemon.io": "https://lemon.io/escape-the-matrix/",
  "Etherscan": "jobs@etherscan.io",
  "Stake Capital": "hr@stake.capital",
  "Coinmarketcap": "https://careers.smartrecruiters.com/B6/",
  "Consensys": "https://consensys.net/open-roles/",
  "Solana Foundation": "https://jobs.ashbyhq.com/solana%20foundation",
  "Bitoasis": "https://careers.smartrecruiters.com/bitoasis",
  "MetaMask": "https://wellfound.com/company/metamask/jobs/",
  "OKEX": "https://wellfound.com/company/okexofficial/jobs/",
  "Bitfinex": "https://bitfinex.recruitee.com/o/",
  "Binance": "https://jobs.lever.co/binance/",
  "Popoo": "hr@popoo.io",
  "Ripple": "https://ripple.com/careers/all-jobs/",
  "Illuvium": "https://illuvium.io/jobs",
  "Swan": "https://swanbitcoin.applytojob.com/",
  "Keyrock": "https://jobs.ashbyhq.com/keyrock/",
  "Coinbase": "https://www.coinbase.com/careers/positions/",
  "Chainlink Labs": "https://wellfound.com/company/chainlink-labs/jobs/",
  "eBay": "https://jobs.ebayinc.com/us/en/job/",
  "Clutchy": "https://apply.workable.com/clutchy-1/",
  "Gnosis": "https://gnosis.jobs.personio.com/",
  "Hang": "https://jobs.ashbyhq.com/Hang/",
  "Rain": "https://jobs.ashbyhq.com/rain",
  "Square": "https://careers.smartrecruiters.com/Square/",
  "Ethereum Address Service (EAS)": "https://careers.smartrecruiters.com/ethereumaddressserviceeas/",
  "Offchain Labs": "https://jobs.lever.co/offchainlabs/",
  "LCX": "https://lcx.freshteam.com/jobs/",
  "Cryptio": "https://jobs.ashbyhq.com/cryptio/",
  "Polygon Labs": "https://jobs.lever.co/Polygon",
  "OpenSea": "https://jobs.lever.co/OpenSea/",
  "GammaSwap": "https://wellfound.com/company/gammaswap/jobs"
}


class Web3CareerSpider(scrapy.Spider):
    name = "web3_career"
    allowed_domains = ["web3.career"]
    start_urls = ["https://web3.career/"]

    def parse(self, response):
        """

        :param response:
        :return:
        """
        post_career_xpath_list = response.xpath('//table[@class="table table-borderless"]/tbody[@class="tbody"]/tr')
        for row in post_career_xpath_list:
            job_dict = {}
            job_tag_list = []
            job_id = row.xpath('./td[1]/div/div/div/a[@style=" text-decoration: none"]').attrib['href']
            job_tag_xpath_list = row.xpath('./td[6]/div/span/a')
            for job_tag_xpath in job_tag_xpath_list:
                job_tag_list.append(job_tag_xpath.root.text[1:-1])
            job_dict["job_id"] = job_id
            job_dict["job_tags"] = job_tag_list
            job_url = f"https://web3.career{job_id}"
            yield scrapy.Request(url=job_url,
                                 dont_filter=True,
                                 callback=self.parse_job_jd,
                                 meta={"job_dict": job_dict})

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

    def parse_job_jd(self, response):
        """
        parse job jd
        :param response:
        :return:
        """
        jd_xpath = response.xpath('//div/script[@type="application/ld+json"]')[0]
        try:
            json_data = json.loads(jd_xpath.root.text)
        except Exception as exc:
            logging.error(f"{jd_xpath}\n\n{exc}\n ")
            return

        company_name = json_data['hiringOrganization']['name']
        if company_name in COMPANY_DICT:
            json_data['apply'] = COMPANY_DICT[company_name]
        else:
            return

        html_xpath_description = response.xpath('//turbo-frame[@id="job"][@target="_top"]/div[@class]/div[@class]/div[@class]/div[@class]/div[@style="word-wrap: break-word;"][@class="text-dark-grey-text p-2 p-md-0 "]')[0].extract()

        json_data['jobId'] = response.meta['job_dict']['job_id']
        json_data['htmlJobDescription'] = html_xpath_description
        json_data['jobTags'] = response.meta['job_dict']['job_tags']
        json_data['sourceUrl'] = response.url
        json_data['fromSource'] = 'web3.career'
        yield json_data


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl web3_career".split()
    cmdline.execute(args)
