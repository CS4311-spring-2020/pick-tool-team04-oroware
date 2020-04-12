import unittest

from EventConfig import EventConfig


class TestEventConfig(unittest.TestCase):
    def test_edit_event_config_valid1(self):
        eventConfig = EventConfig()
        eventConfig.col = eventConfig.db["test_config"]
        self.assertEqual(True, eventConfig.editEventConfig("SQL Attack", "SQL Attack by Red Team", "4/11/2020 1:38 PM", "4/12/2020 1:38 PM"))
        eventConfig.deleteEventConfig()

    def test_edit_event_config_valid2(self):
        eventConfig = EventConfig()
        eventConfig.col = eventConfig.db["test_config"]
        self.assertEqual(True, eventConfig.editEventConfig("SQL Attack", "SQL Attack by Red Team", "4/11/2020 1:38 PM","4/11/2020 1:39 PM"))
        eventConfig.deleteEventConfig()

    def test_edit_event_config_invalid1(self):
        eventConfig = EventConfig()
        eventConfig.col = eventConfig.db["test_config"]
        self.assertEqual(False, eventConfig.editEventConfig("SQL Attack", "SQL Attack by Red Team", "4/12/2020 1:38 PM", "4/11/2020 1:38 PM"))
        eventConfig.deleteEventConfig()

    def test_edit_event_config_invalid2(self):
        eventConfig = EventConfig()
        eventConfig.col = eventConfig.db["test_config"]
        self.assertEqual(False, eventConfig.editEventConfig("SQL Attack", "SQL Attack by Red Team", "4/11/2020 1:38 PM", "4/11/2020 1:38 PM"))
        eventConfig.deleteEventConfig()

    def test_edit_event_config_invalid3(self):
        eventConfig = EventConfig()
        eventConfig.col = eventConfig.db["test_config"]
        self.assertEqual(False, eventConfig.editEventConfig("SQL Attack", "SQL Attack by Red Team", "4/11/2020 1:39 PM", "4/11/2020 1:38 PM"))
        eventConfig.deleteEventConfig()