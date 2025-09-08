import logging
import sys
from pythonjsonlogger import jsonlogger
from src.logger_config import get_logger

logger = get_logger()

def log_metric(logger, entity: str, metric: str, value: int | float):
    """
    Registra métricas de calidad o volumen en el log estructurado.
    """
    logger.info(f"Métrica {entity}.{metric} = {value}",
                extra={"extra_data": {"entity": entity, "metric": metric, "value": value}})

def log_event(logger, event: str, status: str = "OK", details: dict | None = None):
    """
    Registra eventos generales del ETL (ej: inicio, fin, errores).
    """
    logger.info(f"Evento {event} - {status}",
                extra={"extra_data": {"event": event, "status": status, **(details or {})}})


