import asyncio


class AsyncDebouncer:
    def __init__(self, settle_time, callback):
        self.settle_time = settle_time
        self.callback = callback
        self.value = None
        self.timer = None
        self.lock = asyncio.Lock()

    async def update_value(self, new_value):
        async with self.lock:
            if new_value != self.value:
                self.value = new_value
                if self.timer is not None:
                    self.timer.cancel()
                self.timer = asyncio.ensure_future(self._settle_callback())

    async def _settle_callback(self):
        await asyncio.sleep(self.settle_time)
        async with self.lock:
            await self.callback(self.value)