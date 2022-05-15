from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor


tracer = trace.get_tracer(__name__)
resource = Resource.create({SERVICE_NAME: "CMS-FastAPI-BD"})
provider = TracerProvider(resource=resource)


def config_trace_init():
    trace.set_tracer_provider(tracer_provider=provider)
    jaeger_exporter = JaegerExporter(agent_host_name='localhost', agent_port=6831)
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
    # from opentelemetry.sdk._logs import LogEmitterProvider, OTLPHandler, set_log_emitter_provider
    # from opentelemetry.sdk._logs.export import BatchLogProcessor
    # from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
    # trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    # log_emitter_provider = LogEmitterProvider(resource=resource)
    # set_log_emitter_provider(log_emitter_provider)
    #
    # import logging
    # exporter = OTLPLogExporter(insecure=True)
    # log_emitter_provider.add_log_processor(BatchLogProcessor(exporter))
    # log_emitter = log_emitter_provider.get_log_emitter(__name__, "0.1")
    # handler = OTLPHandler(level=logging.NOTSET, log_emitter=log_emitter)
    #
    # logger = logging.getLogger() #.addHandler(handler)
    # logger.addHandler(handler)
    #
    # with tracer.start_as_current_span(f"xxxxxxxxxxxxx") as span:
    #     logger.info("Jackdaws love my big sphinx of quartz.")
    #     logger.debug("Quick zephyrs blow, vexing daft Jim.")
    #     logger.info("How quickly daft jumping zebras vex.")
    #     logger.warning("Jail zesty vixen who grabbed pay from quack.")
    #     logger.error("The five boxing wizards jump quickly.")
