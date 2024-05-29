### LocMemCache

# Django 메모리 캐싱
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-codegenius'
    }
}
