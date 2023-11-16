#scrapy startproject vulnerabilities
# cd vulnerabilities
# scrapy genspider cve cve.mitre.org
# cd vulnerabilities/spiders
# vim cve.py

# run to get website locally
# wget https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html

### sqlite
import scrapy
import os 
import sqlite3


current_dir = os.path.dirname(__file__)
url = os.path.join(current_dir, 'source-EXPLOIT-DB.html')

class CveSpider(scrapy.Spider):
    name = "cve"
    allowed_domains = ["cve.mitre.org"]
    #start_urls = ["https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"]
    start_urls = [f"file://{url}"]

    def parse(self, response):
        connection = sqlite3.connect('vuln.db')
        table = 'CREATE TABLE vulns(exploit TEXT, cve TEXT)'
        cursor = connection.cursor()
        cursor.execute(table)
        connection.commit()
        for child in response.xpath('//table'):
            if len(child.xpath('tr')) > 100:
                table = child
                break
        count = 0
    
        for row in table.xpath('//tr'):
            if count > 100:
                break
            try:
                exploit_id = row.xpath('td//text()')[0].extract()
                cve_id = row.xpath('td//text()')[2].extract()
                cursor.execute('INSERT INTO vulns(exploit, cve) VALUES(?, ?)', (exploit_id, cve_id))
                connection.commit()
                count += 1
            except IndexError:
                pass
    


### sql query
# import scrapy
# import os
# from os.path import dirname

# current_dir = os.path.dirname(__file__)
# url = os.path.join(current_dir, 'source-EXPLOIT-DB.html')
# top_dir = dirname(dirname(dirname(current_dir)))
# sql_file = os.path.join(top_dir, 'sql_files/populate.sql')

# class ExploitSpider(scrapy.Spider):
#     name = 'exploit'
#     allowed_domains = ['cve.mitre.org']
#     # Starting with actual URLs is fine
#     #start_urls = ['http://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html']
#     # But you can use files as well!
#     start_urls = [f"file://{url}"]

#     def parse(self, response):
#         table = None
#         count = 0
#         for child in response.xpath('//table'):
#             if len(child.xpath('tr')) > 100:
#                 table = child
#         for row in table.xpath('//tr'):
#             if count > 100:
#                 break
#             cve_list = []
#             try:
#                 # This captures 1 CVE only, but you may have many
#                 exploit_id = row.xpath('td//text()')[0].extract()
#                 cve_id = row.xpath('td//text()')[2].extract()
#                 print(f"exploit id: {exploit_id} -> {cve_id}")
#                 append_sql_file(exploit_id, cve_id)
# #               # This is one way of doing that
# #                for text in row.xpath('td//text()'):
# #                    if text.extract().startswith('CVE'):
# #                        cve_list.append(text.extract())
# #                print(f"exploit id: {exploit_id} -> {cve_list}")
#             except Exception as err:
#                 print(f"skipping due to: {err}")
#             count += 1


# def append_sql_file(exploit_id, cves):
#     line = f"INSERT INTO exploit(exploit_id, cves) VALUES ('{exploit_id}', '{str(cves)}');\n"
#     if not os.path.exists(sql_file):
#         with open(sql_file, 'w') as _f:
#             _f.write(line)
#         return
#     with open(sql_file, 'a') as _f:
#         _f.write(line)



### json
# import scrapy
# import os 
# import json


# current_dir = os.path.dirname(__file__)
# url = os.path.join(current_dir, 'source-EXPLOIT-DB.html')

# class CveSpider(scrapy.Spider):
#     name = "cve"
#     allowed_domains = ["cve.mitre.org"]
#     #start_urls = ["https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"]
#     start_urls = [f"file://{url}"]

#     def parse(self, response):
#         for child in response.xpath('//table'):
#             if len(child.xpath('tr')) > 100:
#                 table = child
#                 break
#         count = 0
        
#         data = {}
#         json_file = open('vulnerabilities.json', 'w')

#         for row in table.xpath('//tr'):
#             if count > 100:
#                 break
#             try:
#                 exploit_id = row.xpath('td//text()')[0].extract()
#                 cve_id = row.xpath('td//text()')[2].extract()
#                 data[exploit_id] = cve_id
#                 count += 1
#             except IndexError:
#                 pass
#         json.dump(data, json_file)
#         json_file.close()
       

### csv
# import scrapy
# import os 
# import csv


# current_dir = os.path.dirname(__file__)
# url = os.path.join(current_dir, 'source-EXPLOIT-DB.html')

# class CveSpider(scrapy.Spider):
#     name = "cve"
#     allowed_domains = ["cve.mitre.org"]
#     #start_urls = ["https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"]
#     start_urls = [f"file://{url}"]

#     def parse(self, response):
#         for child in response.xpath('//table'):
#             if len(child.xpath('tr')) > 100:
#                 table = child
#                 break
#         count = 0

#         csv_file = open('vulnerabilities.csv', 'w')
#         writer = csv.writer(csv_file)
#         writer.writerow(['exploit id', 'cve id'])
#         for row in table.xpath('//tr'):
#             if count > 100:
#                 break
#             try:
#                 exploit_id = row.xpath('td//text()')[0].extract()
#                 cve_id = row.xpath('td//text()')[2].extract()
#                 writer.writerow([exploit_id, cve_id])
#                 count += 1
#             except IndexError:
#                 pass
#         csv_file.close()