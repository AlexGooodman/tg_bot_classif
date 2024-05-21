# import asyncio
# from aiogram import types
# from aiogram.dispatcher.middlewares.base import BaseMiddleware
# from aiogram.types import Update
# from datetime import datetime, timedelta

# class AntiSpamMiddleware(BaseMiddleware):
#     def __init__(self):
#         super().__init__()
#         self.user_messages = {}

#     async def __call__(self, handler, event: Update, data: dict):
#         if isinstance(event, types.Message):
#             user_id = event.from_user.id
#             message_text = event.text
#             now = datetime.now()

#             if user_id not in self.user_messages:
#                 self.user_messages[user_id] = []

#             # Очистка старых записей
#             self.user_messages[user_id] = [
#                 (msg, timestamp) for msg, timestamp in self.user_messages[user_id]
#                 if now - timestamp < timedelta(seconds=5)
#             ]

#             # Добавляем текущее сообщение
#             self.user_messages[user_id].append((message_text, now))

#             # Проверяем на спам
#             messages_count = len([msg for msg, timestamp in self.user_messages[user_id] if msg == message_text])

#             if messages_count >= 2:
#                 await event.answer("Вы заблокированы за спам на 5 секунд. 😡")
#                 await asyncio.sleep(5)
#                 self.user_messages[user_id] = []
#                 return

#         await handler(event, data)

from aiogram import BaseMiddleware
from aiogram.types import Message
from collections import defaultdict
import time

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        # Хранение последних сообщений пользователя и времени блокировки
        self.user_data = defaultdict(lambda: {"last_message": None, "timestamp": 0, "blocked_until": 0})
    
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        current_time = time.time()
        
        # Получение информации о пользователе
        user_data = self.user_data[user_id]
        last_message = user_data["last_message"]
        last_timestamp = user_data["timestamp"]
        blocked_until = user_data["blocked_until"]
        
        # Проверка на блокировку пользователя
        if current_time < blocked_until:
            return
        
        # Проверка на повторяющиеся сообщения в течение 1 секунды
        if last_message == event.text and current_time - last_timestamp < 1:
            # Установка блокировки на 5 секунд
            self.user_data[user_id]["blocked_until"] = current_time + 5
            await event.answer("<b>Анти-спам:</b> Вы заблокированы на 5 секунд. 😡",
                               parse_mode='HTML')
            return
        
        # Обновление данных о последнем сообщении
        self.user_data[user_id] = {"last_message": event.text, "timestamp": current_time, "blocked_until": blocked_until}
        
        # Продолжение обработки сообщения
        return await handler(event, data)