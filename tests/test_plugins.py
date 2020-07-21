from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from djangocms_column.cms_plugins import ColumnPlugin
from djangocms_column.models import WIDTH_CHOICES


class ColumnTestCase(CMSTestCase):
    def _makeColumn(self, width="10%"):
        placeholder = Placeholder.objects.create(slot="test")
        return add_plugin(placeholder, ColumnPlugin, "en", width=width)

    def test_column_plugin(self):
        """Smoke test adding plugin to placeholder"""
        plugin = self._makeColumn()
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "ColumnPlugin")

    def test_plugin_html(self):
        """
        Ensure plugin renders expected HTML for each width
        """
        for [width, _] in WIDTH_CHOICES:
            with self.subTest(width=width):
                placeholder = Placeholder.objects.create(slot="test")
                model_instance = add_plugin(
                    placeholder, ColumnPlugin, "en", width=width
                )
                renderer = ContentRenderer(request=RequestFactory())

                html = renderer.render_plugin(model_instance, {})

                self.assertInHTML(
                    '<div class="column" style="width: {0}; float: left;">'.format(
                        width
                    ),
                    html,
                )
