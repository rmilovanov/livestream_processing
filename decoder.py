from connect import get_stream_url_from_specs
from models import SimpleProcessor, BufferGenerator
import config


# stream_url, fps = get_stream_url_from_specs()
stream_url, fps = config.stream_url, 30

processor = SimpleProcessor(stream_url)
buffer = BufferGenerator(config.buffer_cap, fps)


while True:
    frame_data = next(processor.frames())
    buffer.put(frame_data)

