import json

from web3_job.settings import redis_tool


def get_web3_career_jobs_all(key='web3.career'):
    """

    :param key:
    :return:
    """
    key_list = redis_tool.get_all(key=key)
    jobs_list = []
    for job_id in key_list:
        job_dict = json.loads(jobs_list[job_id])
        jobs_list.append(job_dict)

    return jobs_list


if __name__ == '__main__':
    get_web3_career_jobs_all()
