import uuid


async def check_user_role(role_id: str):
    if role_id == uuid.UUID('adebb055-9b61-4f59-b1f2-824d007ca6a3'):
        return 'user'
    elif role_id == uuid.UUID('c72909a9-abd1-4903-9b0f-47a2c10e8681'):
        return 'tolk_support'
    elif role_id == uuid.UUID('2777c3c1-d0de-4a08-b13b-03743ec2fbe3'):
        return 'tech_support'
    else:
        return ''
