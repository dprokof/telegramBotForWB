import asyncio
import loader
import logging
import handlers
from utils.set_bot_comands import set_default_commands


async def main():
    await set_default_commands()
    await loader.bot.delete_webhook(drop_pending_updates=True)
    await loader.dp.start_polling(loader.bot, allowed_updates=loader.dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())