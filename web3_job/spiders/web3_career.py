import json
import logging

import scrapy

MAX_PAGE = 15


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
        json_data['jobId'] = response.meta['job_dict']['job_id']
        json_data['jobTags'] = response.meta['job_dict']['job_tags']
        json_data['sourceUrl'] = response.url
        json_data['fromSource'] = 'web3.career'
        yield json_data


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl web3_career".split()
    cmdline.execute(args)
