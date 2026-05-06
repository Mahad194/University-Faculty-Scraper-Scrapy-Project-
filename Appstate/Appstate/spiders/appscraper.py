import scrapy


class AppscraperSpider(scrapy.Spider):
    name = "appscraper"
    # allowed_domains = ["www.appstate.edu"]
    start_urls = ["https://www.appstate.edu/academics/all/"]

    custom_settings = {
        'CONCURRENT_REQUESTS' : 2,
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response):
        table_rows = response.css('tbody tr')
        #make empty list named as department
        department=[]
        for row in table_rows:
            rl = row.css('td:nth-child(2) a::attr(href)').get()
            
            # append rl to empty list
            department.append(rl)
            
                # remove duplicates from department 

        depatrment = list(set(department))
         # make a for loop to request through each url 
        for url in department:
            yield scrapy.Request(url=url, callback=self.parse_faculty)
            

        
           
    def parse_faculty(self, response):
        fac= response.xpath("//a[contains(text(), 'Faculty & Staff')]")
        if fac:
            url = response.xpath("//a[contains(text(), 'Faculty & Staff')]/@href").get()
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_details)
        else:
            return 
        
    def parse_details(self, response):
        tbody = response.css('tbody tr')
        for data in tbody:

           yield{
                "name" : data.css('td.views-field.views-field-title a::text').get(),
                "phone_number" : data.css('div.field-asu-profile-phone div.field-items div.field-item.even::text').get(),
                "email": data.css('div.field-item.even a::text').get(),
                "url" : data.css('h4 a::attr(href)').get(),
            }

        
        
       
        # scrapy.request(url, callback = parse_faculty_and_staff)