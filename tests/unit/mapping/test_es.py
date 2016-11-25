# Copyright 2016: Mirantis Inc.
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

import mock

from health.mapping import es
from tests.unit import test  # noqa


class InitElasticTestCase(test.TestCase):

    @mock.patch("requests.api.request")
    def test_existing_index(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.ok = True
        es.init_elastic("fake-es", "ms_health")
        self.assertEqual(3, mock_request.call_count)
        calls = [mock.call("get", "fake-es/ms_health",
                           allow_redirects=True, params=None)]

        mock_request.assert_has_calls(calls)

    @mock.patch("requests.api.request")
    def test_create_index(self, mock_request):
        mock_request.side_effect = [
            mock.Mock(status_code=404, ok=False),
            mock.Mock(status_code=200, ok=True),
            mock.Mock(status_code=200, ok=True),
            mock.Mock(status_code=200, ok=True),
        ]
        es.init_elastic("fake-es", index_to_create="fake-index")
        calls = [mock.call("get", "fake-es/fake-index", allow_redirects=True,
                           params=None),
                 mock.call("put", "fake-es/fake-index", data=mock.ANY,)
                 ]
        self.assertEqual(4, mock_request.call_count)
        mock_request.assert_has_calls(calls)
