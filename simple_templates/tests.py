from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponse, HttpResponsePermanentRedirect
from django.test import TestCase
from django.test.utils import override_settings

# import the simple_templates middleware and utils modules so that we can
# reload it for each of our testcases, as it needs to reset internal settings
# based on @override_settings() changes.
from simple_templates import middleware, utils


class DefaultTest(TestCase):
    def setUp(self):
        reload(middleware)
        reload(utils)

    def test_nonexistent_template_notfound(self):
        response = self.client.get('/foo/')
        self.assertEqual(type(response), HttpResponseNotFound)

    def test_nonexistent_template_notfound_noslash(self):
        # with no trailing slash and APPEND_SLASH = True, we don't want to redirect
        # to a slash-corrected URL if the simple template doesn't exist - wasted
        # server hit.
        response = self.client.get('/foo')
        self.assertEqual(type(response), HttpResponseNotFound)

    @override_settings(APPEND_SLASH=False)
    def test_nonexistent_template_notfound_noslash_noappendslash(self):
        # we shouldn't redirect at all with APPEND_SLASH=False, no matter what
        response = self.client.get('/foo')
        self.assertEqual(type(response), HttpResponseNotFound)

    def test_template_redirect(self):
        # default settings have APPEND_SLASH = True, so if there is no slash but the
        # template exists, it should redirect to the correct page
        path = u'/test1'
        corrected_path = u'/test1/'
        response = self.client.get(path)
        redirect_location = response.get('Location', u'')

        self.assertEqual(type(response), HttpResponsePermanentRedirect)

        # the redirect location most definitely should not end with the same path as
        # originally requested, otherwise it's redirecting incorrectly (should have a
        # trailing slash)
        self.assertTrue(redirect_location.endswith(corrected_path))

    def test_template_redirect_ab(self):
        # comments from `test_template_redirect` above apply
        path = '/test1?ab=variation1'
        # the corrected path should keep the original query string
        corrected_path = '/test1/?ab=variation1'
        response = self.client.get(path)
        redirect_location = response.get('Location', u'')

        self.assertEqual(type(response), HttpResponsePermanentRedirect)
        self.assertTrue(redirect_location.endswith(corrected_path))

    def test_template_found(self):
        response = self.client.get('/test1/')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')

    def test_template_found_ab(self):
        response = self.client.get('/test1/?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-variation1')

    def test_template_found_ab_nonexistent(self):
        response = self.client.get('/test1/?ab=variation-bad')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')

    @override_settings(APPEND_SLASH=False)
    def test_template_found_noappendslash(self):
        response = self.client.get('/test1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')

    @override_settings(APPEND_SLASH=False)
    def test_template_found_ab_noappendslash(self):
        response = self.client.get('/test1?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-variation1')

    @override_settings(APPEND_SLASH=False)
    def test_template_found_ab_nonexistent_noappendslash(self):
        response = self.client.get('/test1?ab=variation-bad')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')

    def test_page_found(self):
        response = self.client.get(reverse('my-page'))
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'page-original')

    def test_page_found_ab_nonexistent(self):
        response = self.client.get(reverse('my-page') + '?ab=variation-bad')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'page-original')

    def test_page_found_ab(self):
        template = reverse('my-page') + '?ab=variation1'
        response = self.client.get(template)
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'ab_templates-page-variation1')


@override_settings(SIMPLE_TEMPLATES_DIR='st')
class ChangeSimpleTemplatesDirValidTest(TestCase):
    def setUp(self):
        reload(middleware)
        reload(utils)

    def test_template_found(self):
        response = self.client.get('/test1/')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'st-test1')

    def test_template_found_notexistent_ab(self):
        response = self.client.get('/test1/?ab=variation-bad')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'st-test1')

    def test_template_found_ab(self):
        response = self.client.get('/test1/?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'ab_templates-st-variation1')


@override_settings(SIMPLE_TEMPLATES_DIR='st-notfound')
class ChangeSimpleTemplatesDirInValidTest(TestCase):
    def setUp(self):
        reload(middleware)
        reload(utils)

    def test_template_found(self):
        response = self.client.get('/test1/')
        self.assertEqual(type(response), HttpResponseNotFound)


@override_settings(SIMPLE_TEMPLATES_AB_DIR='ab')
class ChangeABTemplatesDirValidTest(TestCase):
    def setUp(self):
        reload(middleware)
        reload(utils)

    def test_template_found_notexistent_ab(self):
        response = self.client.get('/test1/?ab=variation-bad')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')

    def test_template_found_ab(self):
        response = self.client.get('/test1/?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'ab-simple_templates-variation1')

    def test_page_found_ab_nonexistent(self):
        response = self.client.get(reverse('my-page') + '?ab=variation-bad')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'page-original')

    def test_page_found_ab(self):
        template = reverse('my-page') + '?ab=variation1'
        response = self.client.get(template)
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'ab-page-variation1')


@override_settings(SIMPLE_TEMPLATES_AB_DIR='ab-notfound')
class ChangeABTemplatesDirInValidTest(TestCase):
    def setUp(self):
        reload(middleware)
        reload(utils)

    def test_template_ab_notfound(self):
        response = self.client.get('/test1/?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')


@override_settings(SIMPLE_TEMPLATES_AB_PARAM='abtest')
class ChangeABParamTest(TestCase):
    def setUp(self):
        reload(middleware)
        reload(utils)

    def test_template_found_ab_wrongparamname(self):
        response = self.client.get('/test1/?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'simple_templates-test1')

    def test_template_found_ab(self):
        response = self.client.get('/test1/?abtest=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'ab_templates-simple_templates-variation1')

    def test_page_found_ab_nonexistent(self):
        response = self.client.get(reverse('my-page') + '?ab=variation1')
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'page-original')

    def test_page_found_ab(self):
        template = reverse('my-page') + '?abtest=variation1'
        response = self.client.get(template)
        self.assertEqual(type(response), HttpResponse)
        self.assertContains(response, u'ab_templates-page-variation1')
