import structlog
import logging
import sys
import contextvars

# Global ContextVar for Trace ID
trace_id_var = contextvars.ContextVar("trace_id", default=None)

def inject_trace_id(logger, log_method, event_dict):
    """Structlog processor to inject trace_id into every log."""
    trace_id = trace_id_var.get()
    if trace_id:
        event_dict["trace_id"] = trace_id
    return event_dict

def setup_logging(json_logs: bool = False):
    """
    Configures structured logging for the application.
    If json_logs is True, outputs JSON. Otherwise, outputs pretty console logs.
    """
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        inject_trace_id,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if json_logs else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    return structlog.get_logger()
