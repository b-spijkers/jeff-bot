from botsettings.databaseCalls import update_db, select_one_db, insert_db, delete_db

LEGENDARY_COST_MULTIPLIER = 10000
MYTHIC_COST_MULTIPLIER = 1000
RARE_COST_MULTIPLIER = 500
UNCOMMON_COST_MULTIPLIER = 100
COMMON_COST_MULTIPLIER = 10
WACKY_COST_MULTIPLIER = 10000

def add_item_to_user(user_id, item_id, item_quantity):
    add_item = f""" INSERT INTO user_items VALUES ('{user_id}', '{item_id}', '{item_quantity}') """
    insert_db(add_item)
    return f"Added {item_quantity} of item {item_id} to user {user_id}"

def remove_item_from_user(user_id, item_id):
    remove_item = f""" DELETE FROM user_items WHERE user_id = '{user_id}' """
    delete_db(remove_item)
    return f"Removed {item_id} from user {user_id}"

def get_user_items(user_id):
    get_items = f""" SELECT item_id, item_quantity FROM user_items WHERE user_id = '{user_id}' """
    items = select_one_db(get_items)
    return items


