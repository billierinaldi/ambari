#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import alert_disk_space
from mock.mock import patch, MagicMock
from ambari_commons.os_check import OSCheck
from stacks.utils.RMFTestCase import *

from only_for_platform import get_platform, not_for_platform, only_for_platform, PLATFORM_LINUX, PLATFORM_WINDOWS

if get_platform() != PLATFORM_WINDOWS:
  os_distro_value = ('Suse','11','Final')
  from pwd import getpwnam
else:
  #No Windows tests for now, but start getting prepared
  os_distro_value = ('win2012serverr2','6.3','WindowsServer')

class TestAlertDiskSpace(RMFTestCase):
  @patch.object(OSCheck, "os_distribution", new = MagicMock(return_value = os_distro_value))
  @patch('alert_disk_space._get_disk_usage')
  @patch("os.path.isdir")
  @patch.object(OSCheck, "get_os_family", new = MagicMock(return_value = 'redhat'))
  def test_linux_flow(self, isdir_mock, disk_usage_mock):
    isdir_mock.return_value = False

    # / OK, /usr/hdp OK
    disk_usage_mock.return_value = alert_disk_space.DiskInfo(
      total = 21673930752L, used = 5695861760L,
      free = 15978068992L)

    res = alert_disk_space.execute()
    self.assertEqual(res,
      ('OK', ['Capacity Used: [26.28%, 5.7 GB], Capacity Total: [21.7 GB]']))

    # / WARNING, /usr/hdp OK
    disk_usage_mock.return_value = alert_disk_space.DiskInfo(
      total = 21673930752L, used = 14521533603L,
      free = 7152397149L)

    res = alert_disk_space.execute()
    self.assertEqual(res, (
      'WARNING',
      ['Capacity Used: [67.00%, 14.5 GB], Capacity Total: [21.7 GB]']))

    # / CRITICAL, /usr/hdp OK
    disk_usage_mock.return_value = alert_disk_space.DiskInfo(
      total = 21673930752L, used = 20590234214L,
      free = 1083696538)

    res = alert_disk_space.execute()
    self.assertEqual(res, ('CRITICAL',
    ['Capacity Used: [95.00%, 20.6 GB], Capacity Total: [21.7 GB]']))

    # / < 5GB, /usr/hdp OK
    disk_usage_mock.return_value = alert_disk_space.DiskInfo(
      total = 5418482688L, used = 1625544806L,
      free = 3792937882L)

    res = alert_disk_space.execute()
    self.assertEqual(res, ('WARNING', [
      'Capacity Used: [30.00%, 1.6 GB], Capacity Total: [5.4 GB]. Total free space is less than 5.0 GB']))

    # / OK, /usr/hdp WARNING
    disk_usage_mock.side_effect = [
      alert_disk_space.DiskInfo(total = 21673930752L, used = 5695861760L,
        free = 15978068992L),
      alert_disk_space.DiskInfo(total = 21673930752L, used = 14521533603L,
        free = 7152397149L)]

    # trigger isdir(/usr/hdp) to True
    isdir_mock.return_value = True

    res = alert_disk_space.execute()
    self.assertEqual(res, (
      'WARNING', ["Capacity Used: [26.28%, 5.7 GB], Capacity Total: [21.7 GB]. "
                  "Insufficient space at /usr/hdp: Capacity Used: [67.00%, 14.5 GB], Capacity Total: [21.7 GB]"]))

    # / OK, /usr/hdp CRITICAL
    disk_usage_mock.side_effect = [
      alert_disk_space.DiskInfo(total = 21673930752L, used = 5695861760L,
        free = 15978068992L),
      alert_disk_space.DiskInfo(total = 21673930752L, used = 20590234214L,
        free = 1083696538L)]

    res = alert_disk_space.execute()
    self.assertEqual(res, (
      'WARNING', ["Capacity Used: [26.28%, 5.7 GB], Capacity Total: [21.7 GB]. "
                  "Insufficient space at /usr/hdp: Capacity Used: [95.00%, 20.6 GB], Capacity Total: [21.7 GB]"]))

    # / OK, /usr/hdp < 5GB
    disk_usage_mock.side_effect = [
      alert_disk_space.DiskInfo(total = 21673930752L, used = 5695861760L,
        free = 15978068992L),
      alert_disk_space.DiskInfo(total = 5418482688L, used = 1625544806L,
        free = 3792937882L)]

    res = alert_disk_space.execute()
    self.assertEqual(res, (
      'WARNING', ["Capacity Used: [26.28%, 5.7 GB], Capacity Total: [21.7 GB]. "
                  "Insufficient space at /usr/hdp: Capacity Used: [30.00%, 1.6 GB], Capacity Total: [5.4 GB]. Total free space is less than 5.0 GB"]))
