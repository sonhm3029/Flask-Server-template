import logging
from datetime import datetime
from logging import LogRecord
from logging.handlers import HTTPHandler
from typing import Any, Dict, Optional, Tuple

LOGGER_NAME = "FLASK_SERVER"
IVIRSE_LOGGER = logging.getLogger(LOGGER_NAME)
IVIRSE_LOGGER.setLevel(logging.DEBUG)


DEFAULT_FORMATTER = logging.Formatter(
    "%(levelname)s %(name)s %(asctime)s | %(filename)s:%(lineno)d | %(message)s"
)

# Configure console logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(DEFAULT_FORMATTER)
IVIRSE_LOGGER.addHandler(console_handler)


class CustomHTTPHandler(HTTPHandler):
    """Custom HTTPHandler which overrides the mapLogRecords method."""

    # pylint: disable=too-many-arguments,bad-option-value,R1725
    def __init__(
        self,
        identifier: str,
        host: str,
        url: str,
        method: str = "GET",
        secure: bool = False,
        credentials: Optional[Tuple[str, str]] = None,
    ) -> None:
        super(CustomHTTPHandler, self).__init__(host, url, method, secure, credentials)
        self.identifier = identifier

    def mapLogRecord(self, record: LogRecord) -> Dict[str, Any]:
        """Filter for the properties to be send to the logserver."""
        record_dict = record.__dict__
        return {
            "identifier": self.identifier,
            "levelname": record_dict["levelname"],
            "name": record_dict["name"],
            "asctime": record_dict["asctime"],
            "filename": record_dict["filename"],
            "lineno": record_dict["lineno"],
            "message": record_dict["message"],
        }


# Function to configure logging to a file for the current date
def configure_logging_to_file(identifier: str, log_dir: str):
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"{log_dir}/{identifier}_{current_date}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(DEFAULT_FORMATTER)
    IVIRSE_LOGGER.addHandler(file_handler)


def configure(
    identifier: str, log_dir: Optional[str] = None, host: Optional[str] = None
) -> None:
    """Configure logging to file and/or remote log server."""

    # Create formatter
    string_to_input = f"{identifier} | %(levelname)s %(name)s %(asctime)s "
    string_to_input += "| %(filename)s:%(lineno)d | %(message)s"
    formatter = logging.Formatter(string_to_input)

    configure_logging_to_file(identifier, log_dir)

    if host:
        # Create http handler which logs even debug messages
        http_handler = CustomHTTPHandler(
            identifier,
            host,
            "/log",
            method="POST",
        )
        http_handler.setLevel(logging.DEBUG)
        # Override mapLogRecords as setFormatter has no effect on what is send via http
        IVIRSE_LOGGER.addHandler(http_handler)


logger = logging.getLogger(LOGGER_NAME)
log = logger.log
