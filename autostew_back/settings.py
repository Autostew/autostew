import logging

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)


event_poll_period = 1
full_update_period = 5

api_record_destination = "api_record"


api_compatibility = {
    'build_version': [87, 88, 89],
    'lua_version': [301],
    'protocol_version': [135, 136],
}
