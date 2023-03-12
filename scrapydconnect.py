from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://185.209.29.219:6800/')
PROJECT = 'bit28'
#print(scrapyd.list_projects())
#print(scrapyd.list_spiders('bit28'))
#print(scrapyd.schedule('bit28', '28BitSpider'))
print(scrapyd.list_jobs(PROJECT))
