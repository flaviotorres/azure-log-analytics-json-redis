#!/usr/bin/env python3
# Flavio Torres
## save this script as /usr/local/bin/redis_info.py and set the privileges to omsagent:omiusers
## change hostname, port and password accordingly 
## run: 'pip install redis' to get redis lib installed on your local
import json
import redis


def collect_info():
    try:
        redis_db = redis.StrictRedis(host="10.10.10.4", port=5000, db=0, password='*secret*')
        redis_info = redis_db.execute_command('info')
        healthinfo = { 
            "used_memory": redis_info['used_memory'], 
            "used_memory_rss": redis_info['used_memory_rss'],
            "keyspace_hits": redis_info['keyspace_hits'],
            "keyspace_misses": redis_info['keyspace_misses'],
            "expired_keys": redis_info['expired_keys'],
            "evicted_keys": redis_info['evicted_keys'],
            "keys": redis_info['db0']['keys']
            }
        return print (json.dumps(healthinfo))
    except Exception as err:
        err = {"error": err}
        return print (json.dumps(err))

collect_info()
