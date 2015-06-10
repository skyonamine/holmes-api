#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from cow.server import Server
from cow.plugins.sqlalchemy_plugin import SQLAlchemyPlugin
from tornado.httpclient import AsyncHTTPClient
import tornado.locale
from materialgirl import Materializer
from materialgirl.storage.redis import RedisStorage
from tornado_redis_sentinel import SentinelClient

from holmes.handlers.auth import AuthenticateHandler
from holmes.handlers.page import (
    PageHandler, PageReviewsHandler, PageViolationsPerDayHandler, NextJobHandler
)
from holmes.handlers.violation import (
    MostCommonViolationsHandler, ViolationsHandler, ViolationHandler, ViolationDomainsHandler
)
from holmes.handlers.review import (
    ReviewHandler, LastReviewsHandler, ReviewsInLastHourHandler
)
from holmes.handlers.domains import (
    DomainsHandler, DomainDetailsHandler, DomainViolationsPerDayHandler,
    DomainReviewsHandler, DomainsChangeStatusHandler, DomainsFullDataHandler,
    DomainGroupedViolationsHandler, DomainTopCategoryViolationsHandler
)
from holmes.handlers.search import (
    SearchHandler
)
from holmes.handlers.request import (
    RequestDomainHandler, LastRequestsHandler, FailedResponsesHandler,
    LastRequestsStatusCodeHandler
)
from holmes.handlers.limiter import LimiterHandler
from holmes.handlers.domains_violations_prefs import (
    DomainsViolationsPrefsHandler
)
from holmes.handlers.users_violations_prefs import UsersViolationsPrefsHandler
from holmes.handlers.users import UserLocaleHandler

from holmes.handlers.bus import EventBusHandler
from holmes.event_bus import EventBus
from holmes.utils import (
    load_classes, load_languages, locale_path, get_redis
)
from holmes.models import Key, DomainsViolationsPrefs
from holmes.cache import Cache
from holmes import __version__
from holmes.handlers import BaseHandler


def main():
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    HolmesApiServer.run()


class VersionHandler(BaseHandler):
    def get(self):
        self.write(__version__)


class HolmesApiServer(Server):
    def __init__(self, db=None, debug=None, *args, **kw):
        super(HolmesApiServer, self).__init__(*args, **kw)

        self.force_debug = debug
        self.db = db

    def get_extra_server_parameters(self):
        return {
            'no_keep_alive': False
        }

    def initialize_app(self, *args, **kw):
        super(HolmesApiServer, self).initialize_app(*args, **kw)

        self.application.db = None
        self.application.redis = None
        self.application.redis_pub_sub = None

        if self.force_debug is not None:
            self.debug = self.force_debug

    def get_handlers(self):
        uuid_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        domain_regex = r'[a-z0-9]+(?:[\-\.]{1}[a-z0-9]+)*\.[a-z]{2,6}'
        key_name_regex = r'[_a-z0-9\.]+'
        numbers_regex = r'[0-9]+'

        handlers = [
            ('/most-common-violations/?', MostCommonViolationsHandler),
            ('/last-reviews/?', LastReviewsHandler),
            ('/reviews-in-last-hour/?', ReviewsInLastHourHandler, dict(is_public=True)),
            ('/page/(%s)/review/(%s)/?' % (uuid_regex, uuid_regex), ReviewHandler),
            ('/page/(%s)/reviews/?' % uuid_regex, PageReviewsHandler),
            ('/page/(%s)/violations-per-day/?' % uuid_regex, PageViolationsPerDayHandler),
            ('/page/(%s)/?' % uuid_regex, PageHandler),
            ('/search/?', SearchHandler),
            ('/page/?', PageHandler),
            ('/domains/?', DomainsHandler),
            ('/domains-details/?', DomainsFullDataHandler),
            ('/domains/(%s)/?' % domain_regex, DomainDetailsHandler),
            ('/domains/(%s)/violations-per-day/?' % domain_regex, DomainViolationsPerDayHandler),
            ('/domains/(%s)/violations-prefs/?' % domain_regex, DomainsViolationsPrefsHandler),
            ('/domains/(%s)/violations/?' % domain_regex, DomainGroupedViolationsHandler),
            ('/domains/(%s)/violations/(%s)/?' % (domain_regex, numbers_regex), DomainTopCategoryViolationsHandler),
            ('/domains/(%s)/reviews/?' % domain_regex, DomainReviewsHandler),
            ('/domains/(%s)/change-status/?' % domain_regex, DomainsChangeStatusHandler),
            ('/domains/(%s)/requests/(%s)/?' % (domain_regex, numbers_regex), RequestDomainHandler),
            ('/events/?', EventBusHandler),
            ('/violations/?', ViolationsHandler),
            ('/violation/(%s)/?' % key_name_regex, ViolationHandler),
            ('/violation/(%s)/domains/?' % key_name_regex, ViolationDomainsHandler),
            ('/limiters/?', LimiterHandler),
            ('/limiters/(%s)/?' % numbers_regex, LimiterHandler),
            ('/next-jobs/?', NextJobHandler),
            ('/last-requests/?', LastRequestsHandler),
            ('/last-requests/status-code/?', LastRequestsStatusCodeHandler),
            ('/last-requests/failed-responses/?', FailedResponsesHandler),
            ('/version/?', VersionHandler, dict(is_public=True)),
            ('/authenticate/?', AuthenticateHandler, dict(is_public=True)),
            ('/users/violations-prefs/?', UsersViolationsPrefsHandler),
            ('/users/locale/?', UserLocaleHandler),
        ]

        return tuple(handlers)

    def get_plugins(self):
        return [
            SQLAlchemyPlugin,
        ]

    def on_disconnect_redis(self, io_loop, *args, **kwargs):
        self.application.redis.connect(
            sentinels=self.application.config.get('REDIS_SENTINEL_HOSTS'),
            master_name=self.application.config.get('REDIS_MASTER'),
            callback=self.connect_redis(io_loop)
        )

    def on_disconnect_redis_pub_sub(self, io_loop, *args, **kwargs):
        self.application.redis_pub_sub.connect(
            sentinels=self.application.config.get('REDIS_SENTINEL_HOSTS'),
            master_name=self.application.config.get('REDIS_MASTER'),
            callback=self.connect_redis_pub_sub(io_loop)
        )

    def on_connected_redis(self, io_loop):
        self.application.redis.auth(
            self.application.config.get('REDISPASS'),
            callback=lambda *args: self.connect_redis_pub_sub(io_loop)
        )

    def on_connected_redis_pub_sub(self, io_loop):
        def handle(*args, **kwargs):
            def on_auth(*args, **kwargs):
                self.application.event_bus = EventBus(self.application)
                self._after_start(io_loop)

            # FIXME
            if not hasattr(self.application.redis_pub_sub, 'connection_status'):
                return self.connect_redis_pub_sub(io_loop)

            if self.application.redis_pub_sub.connection_status != 'CONNECTED':
                # raise RuntimeError("could not connect to redis...")
                return self.connect_redis_pub_sub(io_loop)

            if self.application.config.get('REDISPASS') is not None:
                self.application.redis_pub_sub.auth(
                    self.application.config.get('REDISPASS'),
                    on_auth
                )
            else:
                on_auth()
        return handle

    def connect_redis(self, io_loop):
        self.application.redis = SentinelClient(
            io_loop=io_loop,
            # disconnect_callback=self.on_disconnect_redis(io_loop)
        )
        self.application.redis.connect(
            sentinels=self.application.config.get('REDIS_SENTINEL_HOSTS'),
            master_name=self.application.config.get('REDIS_MASTER'),
            callback=lambda *args: self.on_connected_redis(io_loop)
        )

    def connect_redis_pub_sub(self, io_loop):
        self.application.redis_pub_sub = SentinelClient(
            io_loop=io_loop,
            # disconnect_callback=self.on_disconnect_redis_pub_sub(io_loop)
        )
        self.application.redis_pub_sub.connect(
            sentinels=self.application.config.get('REDIS_SENTINEL_HOSTS'),
            master_name=self.application.config.get('REDIS_MASTER'),
            callback=self.on_connected_redis_pub_sub(io_loop)
        )

    def after_start(self, io_loop):
        self.connect_redis(io_loop)

    def _after_start(self, io_loop):

        if self.db is not None:
            self.application.db = self.db
        else:
            self.application.db = self.application.get_sqlalchemy_session()

        if self.debug:
            from sqltap import sqltap
            self.sqltap = sqltap.start()

        authnz_wrapper_class = self._load_authnz_wrapper()
        if authnz_wrapper_class:
            self.application.authnz_wrapper = authnz_wrapper_class(self.application.config)
        else:
            self.application.authnz_wrapper = None

        self.application.facters = self._load_facters()
        self.application.validators = self._load_validators()
        self.application.error_handlers = [handler(self.application.config) for handler in self._load_error_handlers()]

        self.application.search_provider = self._load_search_provider()(
            config=self.application.config,
            db=self.application.db,
            authnz_wrapper=self.application.authnz_wrapper,
            io_loop=io_loop
        )

        self.application.fact_definitions = {}
        self.application.violation_definitions = {}

        self.application.default_violations_values = {}

        for facter in self.application.facters:
            self.application.fact_definitions.update(facter.get_fact_definitions())

        Key.insert_keys(self.application.db, self.application.fact_definitions)

        for validator in self.application.validators:
            self.application.violation_definitions.update(validator.get_violation_definitions())

            self.application.default_violations_values.update(
                validator.get_default_violations_values(self.application.config)
            )

        Key.insert_keys(
            self.application.db,
            self.application.violation_definitions,
            self.application.default_violations_values
        )

        self.application.http_client = AsyncHTTPClient(io_loop=io_loop)

        self.application.cache = Cache(self.application)

        self.configure_material_girl()

        self.configure_i18n()

        DomainsViolationsPrefs.insert_default_violations_values_for_all_domains(
            self.application.db,
            self.application.default_violations_values,
            self.application.violation_definitions,
            self.application.cache
        )

    def configure_material_girl(self):
        from holmes.material import configure_materials

        self.redis_material = get_redis(
            self.config.get('MATERIAL_GIRL_SENTINEL_HOSTS'),
            self.config.get('MATERIAL_GIRL_REDIS_MASTER'),
            self.config.get('MATERIAL_GIRL_REDISPASS')
        )

        self.application.girl = Materializer(
            storage=RedisStorage(redis=self.redis_material),
            load_on_cachemiss=self.config.get('MATERIAL_GIRL_LOAD_ON_CACHEMISS', True)
        )

        configure_materials(self.application.girl, self.application.db, self.config)

    def _load_validators(self):
        return load_classes(default=self.config.VALIDATORS)

    def _load_facters(self):
        return load_classes(default=self.config.FACTERS)

    def _load_error_handlers(self):
        return load_classes(default=self.config.ERROR_HANDLERS)

    def _load_authnz_wrapper(self):
        authnz_wrapper_class_name = self.config.get('AUTHNZ_WRAPPER', None)
        if authnz_wrapper_class_name:
            authnz_wrapper_list = load_classes(default=[authnz_wrapper_class_name])
            if isinstance(authnz_wrapper_list, list) and len(authnz_wrapper_list) == 1:
                return authnz_wrapper_list.pop()
        return None

    def _load_search_provider(self):
        search_provider = load_classes(default=[self.config.SEARCH_PROVIDER])
        if isinstance(search_provider, list) and len(search_provider) == 1:
            return search_provider.pop()
        else:
            raise Exception('A search provider must be defined!')

    def before_end(self, io_loop):
        self.application.db.remove()

        if hasattr(self.application, 'redis'):
            del self.application.redis
            logging.info('Disconnecting from redis...')

        if hasattr(self.application, 'redis_pub_sub'):
            del self.application.redis_pub_sub
            logging.info('Disconnecting from redis pubsub...')

        if self.debug and getattr(self, 'sqltap', None) is not None:
            from sqltap import sqltap

            statistics = self.sqltap.collect()
            sqltap.report(statistics, "report.html")

    def configure_i18n(self):
        load_languages()
        tornado.locale.load_gettext_translations(locale_path, 'api')

if __name__ == '__main__':
    main()
