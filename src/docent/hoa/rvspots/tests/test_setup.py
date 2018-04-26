# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from docent.hoa.rvspots.testing import DOCENT_HOA_RVSPOTS_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that docent.hoa.rvspots is properly installed."""

    layer = DOCENT_HOA_RVSPOTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if docent.hoa.rvspots is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'docent.hoa.rvspots'))

    def test_browserlayer(self):
        """Test that IDocentHoaRvspotsLayer is registered."""
        from docent.hoa.rvspots.interfaces import (
            IDocentHoaRvspotsLayer)
        from plone.browserlayer import utils
        self.assertIn(IDocentHoaRvspotsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCENT_HOA_RVSPOTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['docent.hoa.rvspots'])

    def test_product_uninstalled(self):
        """Test if docent.hoa.rvspots is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'docent.hoa.rvspots'))

    def test_browserlayer_removed(self):
        """Test that IDocentHoaRvspotsLayer is removed."""
        from docent.hoa.rvspots.interfaces import \
            IDocentHoaRvspotsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IDocentHoaRvspotsLayer, utils.registered_layers())
