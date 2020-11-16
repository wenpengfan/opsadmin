#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.cache import cache
import functools


def task_lock(**options):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs): 
            cache_key = "task_%s" % func.__name__
            cache_ = cache.get(cache_key)
            if not cache_:
                timeout = options.get('timeout', 0)
                cache.set(cache_key, 'true', timeout)
                try:
                    func(*args, **kwargs)
                finally:
                    cache.delete(cache_key)
        return wrapper
    return decorator
       
