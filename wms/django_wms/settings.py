"""
Django settings for django_wms project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat.apps.ChatConfig',
    'staff.apps.StaffConfig',
    'userprofile.apps.UserprofileConfig',
    'userregister.apps.UserregisterConfig',
    'userlogin.apps.UserloginConfig',
    'inbound.apps.InboundConfig',
    'outbound.apps.OutboundConfig',
    'company.apps.CompanyConfig',
    'supplier.apps.SupplierConfig',
    'asn.apps.AsnConfig',
    'binset.apps.BinsetConfig',
    'binsize.apps.BinsizeConfig',
    'binproperty.apps.BinpropertyConfig',
    'customer.apps.CustomerConfig',
    'capital.apps.CapitalConfig',
    'warehouse.apps.WarehouseConfig',
    'goods.apps.GoodsConfig',
    'goodsunit.apps.GoodsunitConfig',
    'goodsclass.apps.GoodsclassConfig',
    'goodscolor.apps.GoodscolorConfig',
    'goodsbrand.apps.GoodsbrandConfig',
    'goodsshape.apps.GoodsshapeConfig',
    'goodsspecs.apps.GoodsspecsConfig',
    'goodsorigin.apps.GoodsoriginConfig',
    'payment.apps.PaymentConfig',
    'driver.apps.DriverConfig',
    'stock.apps.StockConfig',
    'rest_framework',
    'django_filters',
    'silk',
    'drf_yasg',
    'corsheaders',
    # 'upload'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'django_wms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_wms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_new').replace('\\', '/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

REST_FRAMEWORK = {
    # 文档报错： AttributeError: ‘AutoSchema’ object has no attribute ‘get_link’
    # 用下面的设置可以解决
    #'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    # 默认设置是:
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    # 异常处理器
    'EXCEPTION_HANDLER': 'utils.my_exceptions.custom_exception_handler',
    # Base API policies    　　默认渲染器类
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        #'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 默认解析器类
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    # 1.认证器（全局）
    'DEFAULT_AUTHENTICATION_CLASSES': ['utils.auth.Authtication', ],

    # 2.权限配置（全局）： 顺序靠上的严格
    'DEFAULT_PERMISSION_CLASSES': ["utils.permission.Normalpermission", ],
    # 3.限流（防爬虫）
    'DEFAULT_THROTTLE_CLASSES': ['utils.throttle.VisitThrottle', ],
    # 3.1限流策略
    # 'DEFAULT_THROTTLE_RATES': ['utils.throttle.VisitThrottle', ],

    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': None,
    # 4.分页（全局）：全局分页器, 例如 省市区的数据自定义分页器, 不需要分页
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 每页返回数量
    # 'PAGE_SIZE': 1,  # 默认 None
    # 5.过滤器后端
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'django_filters.rest_framework.backends.DjangoFilterBackend', 包路径有变化
    ],
    # 5.1过滤排序（全局）：Filtering 过滤排序
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'NUM_PROXIES': None,
    # 6.版本控制：Versioning  接口版本控制
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',
    # Authentication  认证
    # 未认证用户使用的用户类型
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    # 未认证用户使用的Token值
    'UNAUTHENTICATED_TOKEN': None,
    # View configuration
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
    # Testing
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',
    # Hyperlink settings
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',
    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,
    # Browseable API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",
    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 86400,
        'OPTIONS': {
            'MAX_ENTRIES': 2000
        }
    }
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token'
)