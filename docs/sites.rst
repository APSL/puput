Sites structure
===============


Multi blog site
---------------
The Wagtail default page architecture it allows to create a tree based CMS where editors could create multiple pages
that are children from others. The Puput architecture also follows this philosophy but you can only create Blog pages
as parents and Entry pages as children. Furthermore all Blog pages must have Root page as parent.

This has a powerful advantage so you can create separated sites with multiple blog instances. For instance, you could create
a simple blog `http://www.example.com/blog/` and another one with videos (a videoblog) `http://www.example.com/tv/`.


Single blog site
----------------

A common case of use is having a site as a blog. In this case, Puput is also good for this purpose.
If you have a site like `http://www.myblog.com` and you want that the root
of the site will be blog page you can modify our Root page on site configuration (`usually here <http://127.0.0.1:8000/blog_admin/sites/1/>`_)
and select the desired blog page. So with this you will be able to go `http://www.myblog.com` instead of
`http://www.myblog.com/blog/`.