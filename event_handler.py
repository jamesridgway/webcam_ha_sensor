import asyncio
import pyinotify


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, debouncer, loop, mqtt_client, topic):
        super().__init__()
        self.debouncer = debouncer
        self.loop = loop
        self.mqtt_client = mqtt_client
        self.topic = topic

    def process_default(self, event):
        if event.pathname.startswith('/dev/video'):
            if event.mask & pyinotify.IN_OPEN:
                asyncio.run_coroutine_threadsafe(self.debouncer.update_value(True), self.loop)
            elif event.mask & pyinotify.IN_CLOSE_WRITE:
                asyncio.run_coroutine_threadsafe(self.debouncer.update_value(False), self.loop)
