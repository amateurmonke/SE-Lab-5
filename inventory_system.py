import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=None):
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

def removeItem(item, qty):
    # Bare except: Changed 'except:' to 'except KeyError:'
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Warning: Attempted to remove item '{item}' which does not exist")
        pass

def getQty(item):
    return stock_data[item]

def loadData(file="inventory.json"):
# Replaced manual open/close with a 'with' block.
# This automatically closes the file even if errors occur.
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"Warning: {file} not found, starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Warning: Could not decode {file}, starting with empty inventory.")
        stock_data = {}
def saveData(file="inventory.json"):
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data, indent=4)) 

def printData():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    # eval("print('eval used')")  # dangerous
    print("Eval commented out")
main()
