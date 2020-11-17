# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

setup(
    name='vedirect',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    setup_requires=['setuptools-git-version'],
    url='https://juju.nz/src/michaelh/vedirect',
    author='Michael Hope',
    author_email='michaelh@juju.nz',
    description='VE.Direct parser and exporter',
    zip_safe=True,
    packages=find_packages(),
    install_requires=[
        'Pint>=0.16.1',
        'click>=7.1.2',
        'paho-mqtt>=1.5.1',
        'prometheus-client>=0.8.0',
        'pyserial>=3.4',
    ],
    entry_points='''
[console_scripts]
vedirect=vedirect.cli:app
    ''',
)
