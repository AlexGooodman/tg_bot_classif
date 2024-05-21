from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from datetime import datetime, timedelta

INACTIVITY_TIMEOUT = 60

class AutoResetFSMMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.last_activity = {}

    async def __call__(self, handler, event, data):
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            now = datetime.now()
            last_activity = self.last_activity.get(user_id)

            if last_activity:
                inactivity_duration = now - last_activity
                if inactivity_duration > timedelta(minutes=INACTIVITY_TIMEOUT):
                    state: FSMContext = data['state']
                    await state.clear()

            self.last_activity[user_id] = now

        data['last_activity'] = now

        return await handler(event, data)
