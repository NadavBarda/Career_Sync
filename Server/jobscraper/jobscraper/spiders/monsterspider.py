import json
import scrapy
from jobscraper.items import JobscraperItem

class MonsterspiderSpider(scrapy.Spider):
    name = "monsterspider"
    
    def __init__(self, *args, **kwargs):
        super(MonsterspiderSpider, self).__init__(*args, **kwargs)
        self.list_len = 18
        self.job = kwargs.get('job', 'Full Stack').title()
        self.type_of_job = kwargs.get('type_of_job', 'full_time').upper()
        self.location = kwargs.get('location', 'San Lorenzo').title()
        self.work_preference = kwargs.get('work_preference', 'Hybrid').title()
        self.experience = kwargs.get('experience', '1')
    
    def start_requests(self):
        url = "https://appsapi.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-US?apikey=AE50QWejwK4J73X1y1uNqpWRr2PmKB3S"
        data = {
            "jobQuery": {
                "query": self.job,
                "employmentTypes":[self.type_of_job],
                "locations": [
                    {
                        "country": "us",
                        "address": self.location,
                        "radius": {
                            "unit": "mi",
                            "value": 20
                        }
                    }
                ]
            },
            "jobAdsRequest": {
                "position": list(range(1, self.list_len + 1)),
                "placement": {
                    "channel": "WEB",
                    "location": "JobSearchPage",
                    "property": "monster.com",
                    "type": "JOB_SEARCH",
                    "view": "SPLIT"
                }
            },
            "fingerprintId": "z150c72f5ac7a9d8ce376f6b50376a99c",
            "offset": self.list_len,
            "pageSize": self.list_len,
            "searchId": "" ,
            "includeJobs": []
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=json.dumps(data),
            callback=self.parse
        )

    def parse(self, response):
        data = json.loads(response.text)
        job_list = data.get('jobResults', [])
        for job_result in job_list:
            job_posting = job_result.get('normalizedJobPosting', {})
            item = self.parse_job(job_posting)
            yield item

    def parse_job(self, job):
        job_item = JobscraperItem()
        job_item['title'] = job['title']
        job_item['url'] = job['url']
        job_item['description'] = job['description']
        job_item['datePosted'] = job['datePosted']
        job_item['organization'] = job['hiringOrganization']['name']
        job_item['jobLocationType'] = job.get('jobLocationType','N/A')
        return job_item
        

