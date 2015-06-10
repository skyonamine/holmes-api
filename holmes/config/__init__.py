#!/usr/bin/python
# -*- coding: utf-8 -*-

from derpconf.config import Config  # NOQA
from holmes.utils import _


MINUTE = 60
HOUR = MINUTE * 60
DAY = 24 * HOUR

Config.define('WORKER_SLEEP_TIME', 10, _('Main loop sleep time'), 'Worker')
Config.define('ZOMBIE_WORKER_TIME', 200,
              _('Time to remove a Worker from API List (must be greater than WORKER_SLEEP_TIME + Validation time)'), 'API')

Config.define('WORKERS_LOOK_AHEAD_PAGES', 10000, _('Number of pages that will be retrieved when looking for the next job'), 'Worker')

Config.define('CONNECT_TIMEOUT_IN_SECONDS', 10, _('Number of seconds a connection can take.'), 'Worker')
Config.define('REQUEST_TIMEOUT_IN_SECONDS', 10, _('Number of seconds a request can take.'), 'Worker')

Config.define('HOLMES_API_URL', 'http://localhost:2368', ('URL that Worker will communicate with API'), 'Worker')
Config.define('HOLMES_WEB_URL', 'http://local.holmes.com:9000', _('URL of the client side application of Holmes'), 'Web')

Config.define('LOG_LEVEL', 'ERROR', 'Default log level', 'Logging')
Config.define('LOG_FORMAT', '%(asctime)s:%(levelname)s %(module)s - %(message)s',
              _('Log Format to be used when writing log messages'), 'Logging')
Config.define('LOG_DATE_FORMAT', '%Y-%m-%d %H:%M:%S',
              _('Date Format to be used when writing log messages.'), 'Logging')

Config.define('FACTERS', [], _('List of classes to get facts about a website'), 'Review')
Config.define('VALIDATORS', [], _('List of classes to validate a website'), 'Review')
Config.define('REVIEW_EXPIRATION_IN_SECONDS', 6 * 60 * 60, _('Number of seconds that a review expires in.'), 'Review')
Config.define('NUMBER_OF_REVIEWS_TO_KEEP', 4, _('Maximum number of reviews to keep'), 'Review')

Config.define('DAYS_TO_KEEP_REQUESTS', 12, _('Number of days to keep requests'), 'Requests')
Config.define('MAX_REQUESTS_FOR_FAILED_RESPONSES', 1000, _('Number of requests for failed responses'), 'Requests')
Config.define('HOLMES_USER_AGENT', 'Mozilla/5.0 (compatible; Holmes)', _('User agent'), 'Requests')

Config.define('MAX_ENQUEUE_BUFFER_LENGTH', 1000,
              _('Number of URLs to enqueue before submitting to the /pages route'), 'Validators')

# Reference data retrieved from HTTP Archive in 06-jan-2014
Config.define('MAX_IMG_REQUESTS_PER_PAGE', 40,
              _('Maximum number of images per page'), 'Image Request Validator')
Config.define('MAX_KB_SINGLE_IMAGE', 26,
              _('Maximum size of a single image'), 'Image Request Validator')
Config.define('MAX_IMG_KB_PER_PAGE', 1028,
              _('Maximum size of images per page'), 'Image Request Validator')
# Reference data retrieved from HTTP Archive in 06-jan-2014
Config.define('MAX_CSS_REQUESTS_PER_PAGE', 8,
              _('Maximum number of external stylesheets per page'), 'CSS Request Validator')
Config.define('MAX_CSS_KB_PER_PAGE_AFTER_GZIP', 46,
              _('Maximum size of stylesheets per page after gzip'), 'CSS Request Validator')

# Reference data retrieved from HTTP Archive in 06-jan-2014
Config.define('MAX_JS_REQUESTS_PER_PAGE', 17,
              _('Maximum number of external scripts per page'), 'JS Request Validator')
Config.define('MAX_JS_KB_PER_PAGE_AFTER_GZIP', 272,
              _('Maximum size of scripts per page after gzip'), 'JS Request Validator')

Config.define('MAX_TITLE_SIZE', 70,
              _('Title tags longer than 70 characters may be truncated in the results'),
              'Title Validator')
Config.define('METATAG_DESCRIPTION_MAX_SIZE', 300,
              _('Description Meta tags longer than 300 characters may be truncated in the results'),
              'Metatag validator')
Config.define('MAX_HEADING_HIEARARCHY_SIZE', 150,
              _('Heading Hierarchy tags longer than 150 characters may be truncated in the results'),
              'Heading Hierarchy Validator')
Config.define('MAX_IMAGE_ALT_SIZE', 70,
              _('Image alt attributes longer than 70 characters may be truncated in the results'),
              'Image Alt Attribute Validator')

Config.define('HTTP_PROXY_HOST', None, _('HTTP Proxy Host to use'), 'Web')
Config.define('HTTP_PROXY_PORT', None, _('HTTP Proxy Port to use'), 'Web')

Config.define('API_PROXY_HOST', None, _('HTTP Proxy Host to use to connect to the API'), 'Web')
Config.define('API_PROXY_PORT', None, _('HTTP Proxy Port to use to connect to the API'), 'Web')

Config.define('COMMIT_ON_REQUEST_END', True, _('Commit on request end'), 'DB')

Config.define('REDIS_MASTER', 'master', _('Redis master'), 'Redis')
Config.define('REDISPASS', None, _('Redis password in case of auth'), 'Redis')
Config.define('REDIS_SENTINEL_HOSTS', ['127.0.0.1:57574'], _('Redis sentinels'),'Redis')

Config.define('MATERIAL_GIRL_REDIS_MASTER', 'master', _('Redis master'), 'Redis')
Config.define('MATERIAL_GIRL_REDISPASS', None, _('Redis password in case of auth'), 'Redis')
Config.define('MATERIAL_GIRL_SENTINEL_HOSTS', ['127.0.0.1:57574'], _('Redis sentinels'), 'Redis')

Config.define('MATERIAL_GIRL_LOAD_ON_CACHEMISS', True, _('Load from database on cache miss'), 'Materializer')

Config.define('REQUIRED_META_TAGS', [], _('List of required meta tags'), 'Meta tag Validator')

Config.define('SCHEMA_ORG_ITEMTYPE', [], _('List of Schema.Org ItemType'), 'Schema.Org ItemType')

Config.define('FORCE_CANONICAL', False, _('Force canonical'), 'Force canonical')

Config.define('BLACKLIST_DOMAIN', [], _('Domain blacklist'), 'Domain blacklist')

Config.define('ERROR_HANDLERS', [], _('List of classes to handle errors'), 'General')

Config.define('SEARCH_PROVIDER', 'holmes.search_providers.noexternal.NoExternalSearchProvider', _('Class to handle searching'), 'Models')

Config.define('ELASTIC_SEARCH_PROTOCOL', 'http', _('ElasticSearch protocol (http|https)'), 'ElasticSearchProvider')
Config.define('ELASTIC_SEARCH_HOST', 'localhost', _('ElasticSearch host'), 'ElasticSearchProvider')
Config.define('ELASTIC_SEARCH_PORT', 9200, _('ElasticSearch port'), 'ElasticSearchProvider')
Config.define('ELASTIC_SEARCH_INDEX', 'holmes', _('ElasticSearch index name'), 'ElasticSearchProvider')

Config.define('ELASTIC_SEARCH_MAX_RETRIES', 3, _('ElasticSearch max number of retries'), 'ElasticSearchProvider')

# SENTRY ERROR HANDLER
Config.define('USE_SENTRY', False, _('If set to true errors will be sent to sentry.'), 'Sentry')
Config.define('SENTRY_DSN_URL', '', _('URL to use as sentry DSN.'), 'Sentry')

Config.define('PAGE_COUNT_EXPIRATION_IN_SECONDS', HOUR, _('Expiration for the cache key for each domain page count'), 'Cache')
Config.define('VIOLATION_COUNT_EXPIRATION_IN_SECONDS', HOUR, _('Expiration for the cache key for each domain violation count'), 'Cache')
Config.define('ACTIVE_REVIEW_COUNT_EXPIRATION_IN_SECONDS', HOUR, _('Expiration for the cache key for each domain violation count'), 'Cache')
Config.define('RESPONSE_TIME_AVG_EXPIRATION_IN_SECONDS', HOUR, _('Expiration for the cache key for each domain average response time'), 'Cache')
Config.define('VIOLATIONS_BY_CATEGORY_EXPIRATION_IN_SECONDS', 6 * 60, _('Expiration for the cache key for each domain violation count by category'), 'Cache')
Config.define('TOP_CATEGORY_VIOLATIONS_EXPIRATION_IN_SECONDS', 6 * 60, _('Expiration for the cache key for each domain top violation in a category'), 'Cache')
Config.define('URL_LOCK_EXPIRATION_IN_SECONDS', 30, _('Expiration for the URL lock for each URL'), 'Cache')
Config.define('NEXT_JOB_URL_LOCK_EXPIRATION_IN_SECONDS', 3 * 60, _('Expiration for the URL lock for next jobs'), 'Cache')
Config.define('NEXT_JOBS_COUNT_EXPIRATION_IN_SECONDS', HOUR, _('Expiration for the cache key for next jobs count'), 'Cache')

materials_expiration_in_seconds = {
    'domains_details': 0.5 * MINUTE + 1,
    'violation_count_for_domains': 4 * MINUTE + 11,
    'violation_count_by_category_for_domains': 3 * MINUTE + 11,
    'top_violations_in_category_for_domains': 5 * MINUTE + 17,
    'blacklist_domain_count': 10 * MINUTE + 1,
    'most_common_violations': HOUR + 7,
    'failed_responses_count': HOUR + 13,
}
Config.define('MATERIALS_EXPIRATION_IN_SECONDS', materials_expiration_in_seconds, 'Expire times for materials', 'material')

materials_grace_period_in_seconds = {
    'domains_details': 2 * materials_expiration_in_seconds['domains_details'],
    'violation_count_for_domains': 2 * materials_expiration_in_seconds['violation_count_for_domains'],
    'violation_count_by_category_for_domains': 2 * materials_expiration_in_seconds['violation_count_by_category_for_domains'],
    'top_violations_in_category_for_domains': 2 * materials_expiration_in_seconds['top_violations_in_category_for_domains'],
    'blacklist_domain_count': 2 * materials_expiration_in_seconds['blacklist_domain_count'],
    'most_common_violations': 2 * materials_expiration_in_seconds['most_common_violations'],
    'failed_responses_count': 2 * materials_expiration_in_seconds['failed_responses_count'],
}
Config.define('MATERIALS_GRACE_PERIOD_IN_SECONDS', materials_grace_period_in_seconds, _('Grace period times for materials'), 'material')

materials_lock_timeout_in_seconds = {
    'domains_details': 3 * materials_grace_period_in_seconds['domains_details'] / 4,
    'violation_count_for_domains': 3 * materials_grace_period_in_seconds['violation_count_for_domains'] / 4,
    'violation_count_by_category_for_domains': 3 * materials_grace_period_in_seconds['violation_count_by_category_for_domains'] / 4,
    'top_violations_in_category_for_domains': 3 * materials_grace_period_in_seconds['top_violations_in_category_for_domains'] / 4,
    'blacklist_domain_count': 3 * materials_grace_period_in_seconds['blacklist_domain_count'] / 4,
    'most_common_violations': 3 * materials_grace_period_in_seconds['most_common_violations'] / 4,
    'failed_responses_count': 3 * materials_grace_period_in_seconds['failed_responses_count'] / 4,
}
Config.define('MATERIALS_LOCK_TIMEOUT_IN_SECONDS', materials_lock_timeout_in_seconds, _('Lock timeouts for materials'), 'material')

Config.define('DEFAULT_PAGE_SCORE', 1, _('Page Score for pages that the user includes through the UI'), 'General')
Config.define('PAGE_SCORE_TAX_RATE', 0.1, _('Default tax rate for scoring pages.'), 'General')

Config.define('REQUEST_CACHE_EXPIRATION_IN_SECONDS', HOUR, _('Expiration in seconds for cache storage of responses.'), 'Cache')

Config.define('MAX_URL_LEVELS', 20, _('Maximum levels of URL'))

Config.define('GOOGLE_CLIENT_ID', None, _('Google client ID'))

Config.define('LIMITER_LOCKS_EXPIRATION', 120, _('The expiration for locks in the limiter'))
Config.define('LIMITER_VALUES_CACHE_EXPIRATION', 600, _('The expiration for values in the limiter'))
Config.define('DEFAULT_NUMBER_OF_CONCURRENT_CONNECTIONS', 5, _('Default number of concurrent connections'), 'Limiter')

Config.define('MOST_COMMON_VIOLATIONS_CACHE_EXPIRATION', 3 * HOUR, _('Expiration for the cache key for the most common violations'), 'Cache')
Config.define('MOST_COMMON_VIOLATIONS_SAMPLE_LIMIT', 50000, _('Limit for the size of the Violation sample used in the aggregation'), 'Violation Handler')
Config.define('TOP_CATEGORY_VIOLATIONS_SAMPLE_LIMIT', 50000, _('Size of the sample used in the top violations of a key category for domains'), 'Domain Handler')

throttling_message_type = {
    'new-request': 5,
    'new-page': 2,
    'new-review': 2,
}
Config.define('EVENT_BUS_THROTTLING_MESSAGE_TYPE', throttling_message_type, _('Throttling by message type'), 'Event Bus')

Config.define('SQLALCHEMY_AUTO_FLUSH', True, _('Defines whether auto-flush should be used in sqlalchemy'))

Config.define('DOMAINS_VIOLATIONS_PREFS_EXPIRATION_IN_SECONDS', HOUR, _('Expiration in seconds for domains violations prefs.'), 'Cache')

Config.define('SECRET_KEY', 'set-a-secret-key', _('Secret key to use in JSON Web Token generation'), 'Sessions')
Config.define('SESSION_EXPIRATION', HOUR, _('Time for Session expiration in seconds'), 'Sessions')
