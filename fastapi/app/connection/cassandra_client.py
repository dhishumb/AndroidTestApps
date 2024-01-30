from cassandra.auth import PlainTextAuthProvider
from ssl import SSLContext, PROTOCOL_TLSv1, CERT_REQUIRED
from cassandra.cluster import Cluster
import base64

def cassandraconnect(config):       
    auth_provider = PlainTextAuthProvider(username=config.cassandra_username, password=base64.b64decode(config.cassandra_password).decode('utf-8'))
    ssl_context = SSLContext(PROTOCOL_TLSv1)
    ssl_context.load_verify_locations(config.cassndra_certlocation)
    ssl_context.verify_mode = CERT_REQUIRED
    cluster = Cluster(contact_points=[config.cassandra_hostname], ssl_context=ssl_context,auth_provider=auth_provider)
    return cluster