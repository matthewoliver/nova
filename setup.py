# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist

import os
import subprocess


class local_sdist(sdist):
    """Customized sdist hook - builds the ChangeLog file from VC first"""

    def run(self):
        if os.path.isdir('.bzr'):
            # We're in a bzr branch
            env = os.environ.copy()
            env['BZR_PLUGIN_PATH'] = os.path.abspath('./bzrplugins')
            log_cmd = subprocess.Popen(["bzr", "log", "--novalog"],
                                       stdout=subprocess.PIPE, env=env)
            changelog = log_cmd.communicate()[0]
            with open("ChangeLog", "w") as changelog_file:
                changelog_file.write(changelog)
        sdist.run(self)

setup(name='nova',
      version='0.9.1',
      description='cloud computing fabric controller',
      author='OpenStack',
      author_email='nova@lists.launchpad.net',
      url='http://www.openstack.org/',
      cmdclass={'sdist': local_sdist},
      packages=find_packages(exclude=['bin', 'smoketests']),
      scripts=['bin/nova-api',
               'bin/nova-compute',
               'bin/nova-dhcpbridge',
               'bin/nova-import-canonical-imagestore',
               'bin/nova-instancemonitor',
               'bin/nova-manage',
               'bin/nova-network',
               'bin/nova-objectstore',
               'bin/nova-rsapi',
               'bin/nova-volume'])
