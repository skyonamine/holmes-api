#!/usr/bin/python
# -*- coding: utf-8 -*-

from mock import Mock, patch, call
from preggy import expect
import json

from holmes.config import Config
from holmes.reviewer import Reviewer
from holmes.facters.phantomas import PhantomasFacter
from holmes.facters.phantomas_info import phantomas_metrics
from tests.unit.base import FacterTestCase
from tests.fixtures import PageFactory


class TestPhantomasFacter(FacterTestCase):

    @patch('subprocess.Popen')  # patch decorator here creates a new Popen object and passes it to the function (http://docs.python.org/dev/library/unittest.mock#unittest.mock.patch)
    def test_can_get_facts(self, popen_mock):
        wait_mock = Mock()
        popen_mock.return_value = Mock(wait=wait_mock, **{'stdout.read': Mock(return_value='{"metrics": {}, "notices": []}')})
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
            'metrics': {
                'foo': 7
            },
            'notices': ['Time spent on backend / frontend: 7% / 7%']
        }
        proc_mock = Mock(**{'stdout.read': Mock(return_value=json.dumps(json_dict))})
        facter.parse_metrics(proc_mock)
        self.assertIn('page.phantomas', facter.review.data)
        self.assertDictEqual(json_dict, facter.review.data['page.phantomas'])
        facter.add_fact.assert_has_calls([
            call(key='page.phantomas.foo', value=7),
            call(key='page.phantomas.notices', value=('7', '7')),
        ], True)

        facter._all_metrics = True
        json_dict = {
            'metrics': {
                'foo': 7
            },
            'notices': ['Foo bar']
        }
        proc_mock = Mock(**{'stdout.read': Mock(return_value=json.dumps(json_dict))})
        facter.parse_metrics(proc_mock)
        self.assertIn('page.phantomas', facter.review.data)
        self.assertDictEqual(json_dict, facter.review.data['page.phantomas'])
        facter.add_fact.assert_has_calls([
            call(key='page.phantomas.foo', value=7),
            call(key='page.phantomas.notices', value=('7', '7')),
            call(key='page.phantomas.foo', value=7),
        ], True)

        json_dict = {
            'metrics': {},
            'notices': []
        }
        proc_mock = Mock(**{'stdout.read': Mock(return_value=json.dumps(json_dict))})
        facter.parse_metrics(proc_mock)
        self.assertIn('page.phantomas', facter.review.data)
        self.assertDictEqual(json_dict, facter.review.data['page.phantomas'])
        facter.add_fact.assert_has_calls([
            call(key='page.phantomas.foo', value=7),
            call(key='page.phantomas.notices', value=('7', '7')),
            call(key='page.phantomas.foo', value=7),
        ], True)

    def test_can_get_fact_definitions(self):
        page = PageFactory.create(url="http://g1.globo.com/1/")

        reviewer = Reviewer(
            api_url='http://localhost:2368',
            page_uuid=page.uuid,
            page_url=page.url,
            config=Config(),
            validators=[]
        )
        facter = PhantomasFacter(reviewer)
        definitions = facter.get_fact_definitions()

        expect('page.phantomas.notices' in definitions).to_be_true()

        expect(definitions).to_length(len(phantomas_metrics) + 1)

        for metric in phantomas_metrics:
            expect('page.phantomas.%s' % metric in definitions).to_be_true()
