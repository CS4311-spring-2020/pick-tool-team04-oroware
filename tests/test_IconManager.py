import unittest

from Icon import Icon
from IconManager import IconManager


class TestIconManager(unittest.TestCase):
    def test_add_icon(self):
        iconManager = IconManager()
        iconManager.col = iconManager.db["test_icons"]
        testIcon1 = Icon()
        testIcon1.name = "Test Icon 1"
        testIcon1.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/testicon1.png"
        self.assertEqual(True, iconManager.addIcon(testIcon1, appInstance=False))
        testIcon2 = Icon()
        testIcon2.name = "Test Icon 2"
        testIcon2.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/testicon2.png"
        self.assertEqual(True, iconManager.addIcon(testIcon2, appInstance=False))
        self.assertEqual(True, "Test Icon 1" in list(iconManager.icons.keys()))
        self.assertEqual(True, "Test Icon 2" in list(iconManager.icons.keys()))
        self.assertEqual(2, len(iconManager.icons.keys()))
        iconManager.deleteStoredconsDb()

    def test_add_icon_invalid(self):
        iconManager = IconManager()
        iconManager.col = iconManager.db["test_icons"]
        testIcon1 = Icon()
        testIcon1.name = "Test Icon 1"
        testIcon1.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/testicon1.png"
        self.assertEqual(True, iconManager.addIcon(testIcon1, appInstance=False))
        self.assertEqual(False, iconManager.addIcon(testIcon1, appInstance=False))
        testIcon2 = Icon()
        testIcon2.name = "Test Icon 2"
        testIcon2.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/testicon2.png"
        self.assertEqual(True, iconManager.addIcon(testIcon2, appInstance=False))
        self.assertEqual(False, iconManager.addIcon(testIcon2, appInstance=False))
        self.assertEqual(True, "Test Icon 1" in list(iconManager.icons.keys()))
        self.assertEqual(True, "Test Icon 2" in list(iconManager.icons.keys()))
        self.assertEqual(2, len(iconManager.icons.keys()))
        iconManager.deleteStoredconsDb()

    def test_delete_icon(self):
        iconManager = IconManager()
        iconManager.col = iconManager.db["test_icons"]
        testIcon1 = Icon()
        testIcon1.name = "Test Icon 1"
        testIcon1.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/testicon1.png"
        iconManager.addIcon(testIcon1, appInstance=False)
        self.assertEqual(True, "Test Icon 1" in list(iconManager.icons.keys()))
        self.assertEqual(1, len(iconManager.icons.keys()))
        self.assertEqual(True, iconManager.deleteIcon("Test Icon 1"))
        self.assertEqual(False, "Test Icon 1" in list(iconManager.icons.keys()))
        self.assertEqual(0, len(iconManager.icons.keys()))
        iconManager.deleteStoredconsDb()

    def test_delete_icon_invalid(self):
        iconManager = IconManager()
        iconManager.col = iconManager.db["test_icons"]
        testIcon1 = Icon()
        testIcon1.name = "Test Icon 1"
        testIcon1.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/testicon1.png"
        iconManager.addIcon(testIcon1, appInstance=False)
        self.assertEqual(True, "Test Icon 1" in list(iconManager.icons.keys()))
        self.assertEqual(1, len(iconManager.icons.keys()))
        self.assertEqual(False, iconManager.deleteIcon("Test Icon 2"))
        self.assertEqual(True, "Test Icon 1" in list(iconManager.icons.keys()))
        self.assertEqual(1, len(iconManager.icons.keys()))
        iconManager.deleteStoredconsDb()


