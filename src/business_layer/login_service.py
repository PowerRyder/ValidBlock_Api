from src.utilities.utils import is_integer
from src.data_access.accounts import login as data_access


def member_id_to_user_id(member_id: str):
    try:
        if not is_integer(member_id):
            return member_id

        dataset = data_access.get_user_id_from_member_id(member_id=int(member_id))

        if len(dataset) > 0 and len(dataset['rs']) > 0:
            if dataset['rs'].iloc[0].loc['success']:
                return dataset['rs'].iloc[0].loc['user_id']
        return member_id
    except Exception as e:
        print(e.__str__())
        return member_id
