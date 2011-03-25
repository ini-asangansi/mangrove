from framework.baseTest import BaseTest

__author__ = 'anandb'
# Copyright 2008-2009 WebDriver committers
# Copyright 2008-2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env python

class ProfileTests(BaseTest) :

    def testGoogleSearch(self):
        self.driver.get("http://www.google.co.in")
        element = self.driver.find_element_by_name("q")
        element.send_keys("Google")
        element.submit()
        print "Title: %s" % self.driver.get_title()
        self.assertIn("Google", self.driver.get_title())


