import logging


class ExtraFieldsFormatter(logging.Formatter):
    def format(self, record):
        # Get values, default to empty string if None
        ip = getattr(record, "ip", None)
        device = getattr(record, "device", None)
        path = getattr(record, "path", None)

        # Construct the message dynamically
        extra_fields = []
        if ip:
            extra_fields.append(f"IP: {ip}")
        if device:
            extra_fields.append(f"Device: {device}")
        if path:
            extra_fields.append(f"Path: {path}")

        # Join the extra fields into a single string
        extra_info = ", ".join(extra_fields)
        if extra_info:
            record.extra_info = f", {extra_info}"
        else:
            record.extra_info = ""

        # Format the log message using the parent's format method
        return super().format(record)
