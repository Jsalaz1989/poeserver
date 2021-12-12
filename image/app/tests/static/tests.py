# type:ignore

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import FirefoxOptions

options = FirefoxOptions()
options.add_argument("--headless")

#EXPECTED_ROOT = '/staticfiles/'
EXPECTED_ROOT = 'https://d337ewj4ohwll8.cloudfront.net'


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/?next=/admin/'))
        links = self.selenium.find_elements_by_xpath('/html/head/link')  ;print(f'links = {links}')
        for link in links:
            href = link.get_attribute('href')   ;print(f'{href=}')
            self.assertIn(EXPECTED_ROOT, href)
