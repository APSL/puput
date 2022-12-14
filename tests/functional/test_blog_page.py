import pytest


@pytest.mark.django_db
class TestBlogPage:

    expected_status_code = 200

    def test_blog_page(self, client, blog_page):
        _, domain, path = blog_page.get_url_parts()
        rq = client.get(f"{domain}{path}")
        assert rq.status_code == self.expected_status_code
        assert blog_page.title in str(rq.content)

    def test_blog_feed_rss(self, client, blog_page):
        _, domain, path = blog_page.get_url_parts()
        rq = client.get(f"{domain}{path}feed/")
        assert rq.status_code == self.expected_status_code
        assert "rss" in str(rq.content)
