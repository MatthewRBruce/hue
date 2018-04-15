# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import

import gcp.gcs

from gcp import conf
from gcp.client import Client
from gcp.gcs.gcsfs import GCSFileSystem

CLIENT_CACHE = None


def get_client(identifier='default'):
  global CLIENT_CACHE
  _init_clients()
  if identifier not in CLIENT_CACHE:
    raise ValueError('Unknown GCS configuration: %s, check you configuration' % identifier)
  return CLIENT_CACHE[identifier]


def _init_clients():
  global CLIENT_CACHE
  if CLIENT_CACHE is not None:
    return
  CLIENT_CACHE = {}
  for identifier in conf.GCS_CONFIGS.keys():
    CLIENT_CACHE[identifier] = _make_client(identifier)


def _make_client(identifier):
  client_conf = conf.GCS_CONFIGS[identifier]
  return Client.from_config(client_conf)


def get_gcsfs(identifier='default'):
   connection = get_client(identifier).get_gcs_connection()
   return GCSFileSystem(connection)