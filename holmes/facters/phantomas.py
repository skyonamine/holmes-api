#!/usr/bin/python
# -*- coding: utf-8 -*-

from holmes.facters import Facter
from holmes.facters.phantomas_info import phantomas_metrics
import json
import subprocess
import re

NOTICES_PATTERN = re.compile(r'Time spent on backend / frontend: (\d+)% / (\d+)%')


class PhantomasFacter(Facter):
    DEFAULTS = {
        'metrics': [],
        'notices': True
    }

    def __init__(self, *args, **kwargs):
        super(PhantomasFacter, self).__init__(*args, **kwargs)
        self._all_metrics = False
        self.config['metrics'] = getattr(self.reviewer.config, 'PHANTOMAS_METRICS', None)
        self.config['notices'] = getattr(self.reviewer.config, 'PHANTOMAS_NOTICES', self.DEFAULTS['notices'])

        if self.config['metrics'] is None:
            self._all_metrics = True
            self.config['metrics'] = self.DEFAULTS['metrics']

    @classmethod
    def get_fact_definitions(cls):
        definitions = {}
        for metric in phantomas_metrics:
            definitions['page.phantomas.%s' % metric] = {
                'title': 'Phantomas metrics - %s' % metric,
                'description': lambda value: '%d' % value
            }
        definitions['page.phantomas.notices'] = {
            'title': 'Phantomas notices - Time spent on backend / frontend',
            'description': lambda value: '%d / %d' % value
        }
        return definitions

    def parse_metrics(self, proc):
        stdout_json = json.load(proc.stdout)
        self.review.data['page.phantomas'] = stdout_json

        if self._all_metrics:
            self.config['metrics'] = stdout_json['metrics'].keys()

        for metric in self.config['metrics']:
            self.add_fact(
                key='page.phantomas.%s' % metric,
                value=stdout_json['metrics'][metric]
            )

        if self.config['notices']:
            matches = NOTICES_PATTERN.match(' '.join(stdout_json['notices']))
            if matches:
                self.add_fact(
                    key='page.phantomas.notices',
                    value=matches.groups()
                )

    def get_facts(self):
        ph_cmd = 'phantomas --url=%s --format=json' % self.page_url
        proc = subprocess.Popen([ph_cmd], shell=True, bufsize=-1, stdout=subprocess.PIPE)
        proc.wait()
        self.parse_metrics(proc)
