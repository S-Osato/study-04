### 商品クラス
from xxlimited import Null
from numpy import quantile
from pyparsing import null_debug_action
import os
import csv
import pandas as pd

class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price
    
    def get_item_code(self):
        return self.item_code
    
    def get_item_name(self):
        return self.item_name

class Receipt:
    def __init__(self):
        self.text = ''
    
    def add_text(self, text):
        self.text = f'{self.text}{text}\n'

    def print_receipt(self):
        print(self.text)
        
    def write_receipt(self):
        path = "receipt.txt"
        with open(path, mode='w') as text_file:
            text_file.write(self.text)
        
### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
        self.sum = 0
        self.recipt = Receipt()
    
    def add_item_order(self,item_code, item_quantity):
        self.item_order_list.append({'code': item_code, 'quantity': item_quantity})
        
    def search_item(self, item_code):
        for item in self.item_master:
            if item.get_item_code() == item_code:
                return item
        return Null
        
    def add_order_console(self):
        while True:
            item_code = input("商品コードを入力してください。 >>> ")
            item_quantity = input("個数入力してください。 >>> ")
            self.add_item_order(item_code, item_quantity)
            
            if 'y' != input("続けて登録しますか？ y/n >>> "):
                break
            
    def create_recipt(self):
        for item in self.item_order_list:
            searched_item = self.search_item(item['code'])
            price = int(searched_item.get_price())
            quantity = int(item['quantity'])
            
            item_name_text = "商品名:{}".format(searched_item.get_item_name())
            item_price_text = "価格:{}".format(price)
            item_quantity_text = "個数:{}".format(quantity)
            
            self.recipt.add_text(f"{item_name_text} {item_price_text} {item_quantity_text}")
            
            self.sum +=  price * quantity
        
        sum_text = "合計金額:{}".format(self.sum)
        self.recipt.add_text(f"{sum_text}")

    def print_receipt(self):
        self.recipt.print_receipt()
        
    def checkout(self):
        payment = int(input("お預かり金額を入力してください。 >>> "))
        change =  payment - self.sum
        if change > 0:
            print(f"お釣り:{change}")
            self.recipt.add_text(f"お釣り:{change}")
        else:
            print("金額がたりません")
        
    def write_receipt(self):
        self.recipt.write_receipt()
        
def register_item_master_from_csv(csv_path, item_master):
    if os.path.exists(csv_path):
        print(f"{csv_path}をアイテムマスタに登録します。")
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                item_master.append(Item(row[0], row[1], row[2]))
    else:
        print("アイテムマスタがありません。")
        
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    
    csv_path = "source.csv"
    register_item_master_from_csv(csv_path, item_master)
    
    # オーダー登録
    order=Order(item_master)
    
    order.add_order_console()
    
    order.create_recipt()
    order.print_receipt()
    
    order.checkout()
    order.write_receipt()
    
if __name__ == "__main__":
    main()