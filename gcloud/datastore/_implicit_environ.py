# Copyright 2014 Google Inc. All rights reserved.
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

"""Module to provide implicit behavior based on enviroment.

Acts as a mutable namespace to allow the datastore package to
imply the current dataset ID and connection from the enviroment.
"""

import httplib2
import socket

try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None


DATASET_ID = None
"""Module global to allow persistent implied dataset ID from enviroment."""

CONNECTION = None
"""Module global to allow persistent implied connection from enviroment."""


def app_engine_id():
    """Gets the App Engine application ID if it can be inferred.

    :rtype: string or ``NoneType``
    :returns: App Engine application ID if running in App Engine,
              else ``None``.
    """
    if app_identity is None:
        return None

    return app_identity.get_application_id()


def compute_engine_id():
    """Gets the Compute Engine project ID if it can be inferred.

    Uses 169.254.169.254 for the metadata server to avoid request
    latency from DNS lookup.

    See https://cloud.google.com/compute/docs/metadata#metadataserver
    for information about this IP address. (This IP is also used for
    Amazon EC2 instances, so the metadata flavor is crucial.)

    See https://github.com/google/oauth2client/issues/93 for context about
    DNS latency.

    :rtype: string or ``NoneType``
    :returns: Compute Engine project ID if the metadata service is available,
              else ``None``.
    """
    http = httplib2.Http(timeout=0.1)
    uri = 'http://169.254.169.254/computeMetadata/v1/project/project-id'
    headers = {'Metadata-Flavor': 'Google'}

    response = content = None
    try:
        response, content = http.request(uri, method='GET', headers=headers)
    except socket.timeout:
        pass

    if response is None or response['status'] != '200':
        return None

    return content