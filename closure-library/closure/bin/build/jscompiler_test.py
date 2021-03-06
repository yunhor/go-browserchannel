#!/usr/bin/env python
#
# Copyright 2013 The Closure Library Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Unit test for depstree."""

__author__ = 'nnaze@google.com (Nathan Naze)'


import unittest

import jscompiler


class JsCompilerTestCase(unittest.TestCase):
  """Unit tests for jscompiler module."""

  def testGetJsCompilerArgs(self):

    args = jscompiler._GetJsCompilerArgs(
        'path/to/jscompiler.jar',
        1.6,
        ['path/to/src1.js', 'path/to/src2.js'],
        ['--test_jvm_flag'],
        ['--test_compiler_flag']
        )

    self.assertEqual(
        ['java', '-client', '--test_jvm_flag',
         '-jar', 'path/to/jscompiler.jar',
         '--js', 'path/to/src1.js',
         '--js', 'path/to/src2.js', '--test_compiler_flag'],
        args)

    args = jscompiler._GetJsCompilerArgs(
        'path/to/jscompiler.jar',
        1.7,
        ['path/to/src1.js', 'path/to/src2.js'],
        ['--test_jvm_flag'],
        ['--test_compiler_flag'])

    self.assertEqual(
        ['java', '-d32', '-client', '--test_jvm_flag',
         '-jar', 'path/to/jscompiler.jar',
         '--js', 'path/to/src1.js',
         '--js', 'path/to/src2.js',
         '--test_compiler_flag'],
        args)

    self.assertRaises(
        jscompiler.JsCompilerError,
        lambda: jscompiler._GetJsCompilerArgs(
            'path/to/jscompiler.jar',
            1.5,
            ['path/to/src1.js', 'path/to/src2.js'],
            ['--test_jvm_flag'],
            ['--test_compiler_flag']))

  def testGetJavaVersion(self):

    def assertVersion(expected, version_string):
      self.assertEquals(expected, version_string)

      assertVersion(1.7, _TEST_JAVA_VERSION_STRING)
      assertVersion(1.4, 'java version "1.4.0_03-ea"')


_TEST_JAVA_VERSION_STRING = """\
openjdk version "1.7.0-google-v5"
OpenJDK Runtime Environment (build 1.7.0-google-v5-64327-39803485)
OpenJDK Server VM (build 22.0-b10, mixed mode)
"""


if __name__ == '__main__':
  unittest.main()
