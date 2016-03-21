import time


class TestBlogPage(object):

    def test_blog_page_home(self, browser, site_url):
        browser.visit(site_url + '/blog/')
        assert browser.status_code == 200
        assert browser.is_text_present('Blog')

    def test_blog_page_click_search(self, browser, site_url):
        browser.visit(site_url + '/blog/')
        browser.fill('q', 'test')
        button = browser.find_by_css('.btn-default')[0]
        button.click()
        time.sleep(2)
        assert browser.url == site_url + '/blog/search/?q=test'
        assert browser.status_code == 200
        assert browser.is_text_present('Entries for search')
