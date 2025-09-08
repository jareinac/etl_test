import logging
import json
from pathlib import Path

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        if record.__dict__.get("extra_data"):
            log_record.update(record.__dict__["extra_data"])
        return json.dumps(log_record)

def get_logger(name="etl", log_dir="logs", log_file="etl_log.json"):
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:  # evita duplicados
        # Handler a archivo JSON
        fh = logging.FileHandler(Path(log_dir) / log_file)
        fh.setFormatter(JsonFormatter())
        logger.addHandler(fh)

        # Handler a consola
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(ch)

    return logger
