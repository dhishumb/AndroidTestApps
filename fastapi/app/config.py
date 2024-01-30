from functools import lru_cache
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    elastic_hostname: str = "itclusteres.us.bank-dns.com"
    elastic_username: str = "ctappdev"
    elastic_password: str = "5m6VtLAg2J8mP93M"
    elastic_port: str = "9200"
    elastic_index: str = "usb-ct-it1*"
    elastic_certlocation = os.path.join(os.getcwd(), "app", "ssl", "usbtrust.pem")
    elastic_resultsize = 10
    pingurl: str = "https://it-federation.usbank.com/as/token.oauth2"
    pingclientid = "CTTenant1"
    pingclientpassword = (
        "g4Rb0QiZUim9AFWMIQJ8JRAtO6SqxnBQ6tPpIYxQ94DGrFv8f3kAqb0T1Wd5R47p"
    )
    cassandra_hostname = "10.127.235.140"
    cassandra_username = "ctappdev"
    cassandra_password = "cm9TZTdsU3d1dDQ5"
    cassndra_certlocation = os.path.join(os.getcwd(), "app", "ssl", "usbtrust.pem")
    cassandra_datacenter = "datacenter"

    class Config:
        env_prefix = "APP_"


@lru_cache()
def get_setting():
    return Settings()