import json
import logging


class StructuredJsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "message": record.getMessage(),
            "level": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "logger": record.name,
        }
        # Include extra fields if available
        if hasattr(record, "extras"):
            log_obj.update(record.extras)
        return json.dumps(log_obj)
