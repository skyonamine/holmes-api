#!/usr/bin/python
# -*- coding: utf-8 -*-

from mock import Mock, patch, call
from preggy import expect
import json

from holmes.config import Config
from holmes.reviewer import Reviewer
from holmes.facters.phantomas import PhantomasFacter
from tests.unit.base import FacterTestCase
from tests.fixtures import PageFactory


class TestPhantomasFacter(FacterTestCase):

    @patch('subprocess.Popen')
    def test_get_facts(self, popen_mock):
        wait_mock = Mock()
        popen_mock.return_value = Mock(wait=wait_mock, **{'stdout.read': Mock(return_value='{"metrics": {}, "notices": []}')})
        popen_mock.wait = Mock()
        page = PageFactory.create(url="http://g1.globo.com/1/")

        reviewer = Reviewer(
            api_url='http://localhost:2368',
            page_uuid=page.uuid,
            page_url=page.url,
            config=Config(),
            validators=[]
        )
        facter = PhantomasFacter(reviewer)
        facter.add_fact = Mock()

        facter.get_facts()

        popen_mock.assert_called_once_with(
            ['phantomas --url=http://g1.globo.com/1/ --format=json'],
            shell=True,
            bufsize=-1,
            stdout=-1
        )
        wait_mock.assert_called_once_with()

    def test_parse_metrics(self):
        page = PageFactory.create(url="http://g1.globo.com/1/")

        reviewer = Reviewer(
            api_url='http://localhost:2368',
            page_uuid=page.uuid,
            page_url=page.url,
            config=Config(),
            validators=[]
        )
        facter = PhantomasFacter(reviewer)
        facter.add_fact = Mock()

        json_dict = {
            "metrics": {
                "foo": 7
            },
            "notices": ["Time spent on backend / frontend: 7% / 7%"]
        }
        proc_mock = Mock(**{'stdout.read': Mock(return_value=json.dumps(json_dict))})
        facter.parse_metrics(proc_mock)
        self.assertIn('page.phantomas', facter.review.data)
        self.assertDictEqual(json_dict, facter.review.data['page.phantomas'])
        facter.add_fact.assert_called_with(
            key=u'page.phantomas.foo',
            value=7
        )
        facter.add_fact.assert_called_with(
            key='page.phantomas.notices',
            value=(u'7', u'7')
        )


        # facter._all_metrics = True
        # return_value = '''{
        #     'metrics': {
        #         'foo': 7
        #     },
        #     'notices': ['Foo bar']
        # }'''
        # proc_mock = Mock(**{'stdout.read': Mock(return_value=return_value)})
        # facter.parse_metrics(proc_mock)

        # return_value = '''{
        #     'metrics': {},
        #     'notices': []
        # }'''
        # proc_mock = Mock(**{'stdout.read': Mock(return_value=return_value)})
        # facter.parse_metrics(proc_mock)

