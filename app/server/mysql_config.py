from decouple import config


def mysql_connection_config():
    return {
        "host": config("MYSQL_HOST", default="localhost"),
        "user": config("MYSQL_USER", default="ztrack2023"),
        "passwd": config("MYSQL_PASSWORD", default="lpmp2018"),
        "database": config("MYSQL_DATABASE", default="zgroupztrack"),
    }
