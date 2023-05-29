#!/usr/bin/env python3
"""
filtered logger
"""
import logging
import mysql.connector
import os
import re
from typing import (
    List,
    Sequence,
)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns the log message obfuscated, and joined with seperator
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence[str] = None) -> None:
        """Initialize new instance of RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        message = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to MySQL database"""
    USER = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    PASSWORD = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    HOST = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DATABASE = os.getenv("PERSONAL_DATA_DB_NAME")
    connector = mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DATABASE
    )
    return connector


def main() -> None:
    """returns none"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={}; ip={}; \
                    last_login={}; user_agent={}; "\
                    .format(row[0], row[1],
                            row[2], row[3], row[4], row[5], row[6], row[7])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
