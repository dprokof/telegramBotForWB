from utils.database.schemas.users import User


async def add_user(user_id: int, user_name: str):
    try:
        user = User(user_id=user_id, user_name=user_name)