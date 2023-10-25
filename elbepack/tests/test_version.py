# ELBE - Debian Based Embedded Rootfilesystem Builder
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020 Linutronix GmbH

import unittest

from elbepack.version import elbe_version

# Since this is just an example on how to make tests, we skip them
class TestElbepackVersion(unittest.TestCase):

    # This is a read-only state that is the same for every tests
    expected_version = "14.9.2"

    def setUp(self):
        # This is a mutable state that is different for every tests
        self.my_list = []

    def tearDown(self):
        # You might want to cleanup your mutable states here
        pass

    def test_version(self):
        self.my_list.append(1)
        self.assertEqual(elbe_version, self.expected_version)
