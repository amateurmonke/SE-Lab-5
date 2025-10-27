import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    if logs is None:
        logs = []
    if not item:
        return
    if not isinstance(qty, int):
        return
    if not isinstance(item, str):
        return
    stock_data[item] = stock_data.get(item, 0) + qty

    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))


def remove_item(item, qty):
    # Bare except: Changed 'except:' to 'except KeyError:'
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(
            f"Warning: Attempted to remove item '{item}' which does not exist"
        )
        pass


def get_qty(item):
    return stock_data[item]


def load_data(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"Warning: {file} not found, starting with empty inventory")
        stock_data = {}
    except json.JSONDecodeError:
        print(
            f" Warning: Could not decode {file}, starting with empty inventory"
        )
        stock_data = {}


def save_data(file="inventory.json"):
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data, indent=4))


def print_data():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])


def check_low_items(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result


def main():
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, no check
    remove_item("apple", 3)
    remove_item("orange", 1)
    # Now safely returns 0 for "apple"
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    # eval("print('eval used')")  # dangerous
    print("Eval commented out")


main()
