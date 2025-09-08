from src.logger_config import get_logger
from src.logging_utils import log_metric, log_event

logger = get_logger()
   
def main():
    log_event(logger, "ETL Job", "START")
    log_metric(logger,"dim_user", "records", 5)
    log_event(logger, "ETL Job", "FIN")

if __name__ == "__main__":
    main()