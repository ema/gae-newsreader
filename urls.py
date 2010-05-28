# Copyright 2008 Google Inc.
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

from django.conf.urls.defaults import *

USERID_VALID_CHARS = '[\w@.]'

urlpatterns = patterns('feeds.views',
    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
    #(r'^admin/', include('django.contrib.admin.urls')),
    (r'^(?P<username>%s+)/addfeed/' % USERID_VALID_CHARS, 'add_feed'),
    (r'^(?P<username>%s+)/(?P<feed_key>[\w-]+)/removesub/' % USERID_VALID_CHARS, 'remove_feed'),
    (r'^(?P<username>%s+)/(?P<feed_key>[\w-]+)/' % USERID_VALID_CHARS, 'render_feed'),
    (r'^(?P<username>%s+)/' % USERID_VALID_CHARS, 'user_feeds'),
    (r'', 'homepage'),
)
