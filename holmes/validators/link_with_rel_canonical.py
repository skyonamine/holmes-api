#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse

from holmes.validators.base import Validator


class LinkWithRelCanonicalValidator(Validator):

    @classmethod
    def get_absent_meta_canonical_message(cls, value):
        url = 'https://support.google.com/webmasters/answer/139394?hl=en'
        return 'As can be seen in this page <a href="%s">About ' \
               'rel="canonical"</a>, it\'s a good practice to ' \
               'include rel="canonical" urls in the pages for ' \
               'your website.' % url

    @classmethod
    def get_violation_definitions(cls):
        return {
            'absent.meta.canonical': {
                'title': 'Link with rel="canonical" not found',
            }
        }

    def validate(self):
        if not self.config.FORCE_CANONICAL:
            # Only pages with query string parameters
            if self.page_url:
                if not urlparse(self.page_url).query:
                    return

        head = self.get_head()
        canonical = [item for item in head if item.get('rel') == 'canonical']

        if not canonical:
            self.add_violation(
                key='absent.meta.canonical',
                value='',
                points=30
            )

    def get_head(self):
        return self.review.data.get('page.head', None)