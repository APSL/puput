import pytest
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker
from wagtail.models import Locale, Page, Site

from puput.models import BlogPage, Category, EntryPage, Tag

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def locale(settings):
    yield baker.make(Locale, language_code=settings.LANGUAGE_CODE)


@pytest.fixture
def root_page(locale):
    # delete pre existent pages to avoid tree problems and page collisions
    Page.objects.all().delete()
    root_page = Page(title="root_page", slug="root_page", depth=1, path="0001", live=True, locale=locale)
    root_page.save()
    baker.make(Site, root_page=root_page, hostname="localhost", is_default_site=True, port=8000)
    yield root_page


@pytest.fixture
def blog_page(root_page):
    content_type = ContentType.objects.get_for_model(BlogPage)
    blogpage = BlogPage(
        title="Puput blog",
        slug="blog",
        content_type=content_type,
        locale=root_page.locale,
    )
    root_page.add_child(instance=blogpage)
    blogpage.save()
    yield blogpage


@pytest.fixture
def author():
    yield baker.make(User)


@pytest.fixture
def category():
    yield baker.make(Category)


@pytest.fixture
def tag():
    yield baker.make(Tag)


@pytest.fixture
def entry_page(blog_page, author, category, tag):
    content_type = ContentType.objects.get_for_model(EntryPage)
    entrypage = EntryPage(
        title="Puput entry",
        slug="entry",
        content_type=content_type,
        locale=blog_page.locale,
        body="body",
        owner=author,
    )
    blog_page.add_child(instance=entrypage)
    entrypage.save()
    entrypage.categories.add(category)
    entrypage.tags.add(tag)
    yield entrypage
