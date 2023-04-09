import json

from web3_job.settings import redis_tool


def get_web3_career_jobs_all(key='web3.career') -> list:
    """

    :param key:
    :return:
    """
    key_list = redis_tool.get_all(key=key)
    jobs_list = []
    for job_id in key_list:
        job_dict = json.loads(key_list[job_id])
        jobs_list.append(job_dict)

    return jobs_list


def get_web3_career_company_all(key='web3.career') -> dict:
    """

    :param key:
    :return:
    """
    jobs_list = get_web3_career_jobs_all(key=key)
    companys_dict = {}
    for job_dict in jobs_list:
        if job_dict['hiringOrganization']['name'] not in companys_dict:
            companys_dict[job_dict['hiringOrganization']['name']] = job_dict['sourceUrl']
    return companys_dict


if __name__ == '__main__':
    tem_jobs_list = get_web3_career_jobs_all()
    for row in tem_jobs_list:
        print(row['sourceUrl'], row['jobId'])
    tem_companys_dict = get_web3_career_company_all()
    print(len(tem_companys_dict))
    for row in tem_companys_dict:
        print(row, tem_companys_dict[row])
