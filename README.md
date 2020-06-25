# halalmas
halalmas.marikoding.com


how to start
---------------

$ cd /home/herman3g/marikoding/source/halalmas/app/src/halalmas
$ ln -s /home/herman3g/marikoding/source/credentials/halalmas/settings/ settings

$ cd /home/herman3g/marikoding/source/halalmas/app/src/
$ ln -s /home/herman3g/marikoding/source/credentials/halalmas/postactivate/postactivate_crm postactivate_crm
$ ln -s /home/herman3g/marikoding/source/credentials/halalmas/postactivate/postactivate_me postactivate_me


$vim /home/herman3g/.virtualenvs/marikoding_halalmas/lib/python3.6/site-packages/dal/views.py
change line 10
from django.utils import six  -to- import six

$vim /home/herman3g/.virtualenvs/marikoding_halalmas/lib/python3.6/site-packages/dal/widgets.py
change line 14
from django.utils import six  -to- import six

$ vim vim /home/herman3g/.virtualenvs/marikoding_halalmas/lib/python3.6/site-packages/dal_select2/widgets.py
change line 17
from django.utils import six  -to- import six

$ vim /home/herman3g/.virtualenvs/marikoding_halalmas/lib/python3.6/site-packages/dal_select2/views.py
change line 10
from django.utils import six  -to- import six