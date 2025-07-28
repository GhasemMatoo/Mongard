import scrapy


class FormgithubSpider(scrapy.Spider):
    name = "FormGithub"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/login"]

    def parse(self, response):
        data = {'login': 'matoogsm90@gmail.com', 'password': 'M9119163658g'}

        for hidden in response.css('input[type="hidden"]'):
            data[hidden.attrib['name']] = hidden.attrib.get('value', 'unknow')

        return scrapy.FormRequest.from_response(
            response=response, url='https://github.com/session', formdata=data, callback=self.after_login)

    def after_login(self, response):
        yield response.follow('https://github.com/GhasemMatoo', self.profile)

    def profile(self, response):
        yield {'info': response.css(
            'body > div.logged-in.env-production.page-responsive.page-profile.mine >'
            ' div.application-main > main > div > div > div.Layout-sidebar > div > div >'
            ' div.d-flex.flex-column > div.js-profile-editable-area.d-flex.flex-column.d-md-block >'
            ' div.flex-order-1.flex-md-order-none.mt-2.mt-md-0 > div > a:nth-child(2) > span::text').get()}
