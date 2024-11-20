import json
import os.path
import pandas as pd
import IPython 
import datetime
from datetime import timedelta
import getpass
available_equipments={
    1:{"Equipment_name":"Throwing balls",
       "Category":"Short put",
       "Price":100,
       "Quantity":10,
       "Date":"28/04/2024"},
    2:{"Equipment_name":"Baton",
       "Category":"Relay",
       "Price":50,
       "Quantity":10,
       "Date":"28/04/2024"},
    3:{"Equipment_name":"Pole Vault Poles",
       "Category":"Pole Vault",
       "Price":3000,
       "Quantity":10,
       "Date":"28/04/2024"},
    4:{"Equipment_name":"Hurdles",
       "Category":"Hurdles",
       "Price":2500,
       "Quantity":10,
       "Date":"28/04/2024"},
    5:{
        "Equipment_name":"Javelin",
       "Category":"Javelin Throw",
       "Price":2000,
       "Quantity":10,
       "Date":"28/04/2024"
    }
}
def admin():
    print("WELCOME TO ATHLETIC EQUIPMENT INVENTORY")
    p="password"
    password = getpass.getpass("Enter password: ")

    #print("Password entered:", password) 
    if password==p:
        while 1:
            print("1.Display equipments with their details\n2.Insert equipments\n3.Delete Equipments\n4.Display User reports\n5.Exit\nEnter your choice:")
            n=int(input())
            if n==1:
                display_data()
            if n==2:
                insert_equipments()
            if n==3:
                delete_equipments()
            if n==4:
                display_user_reports()
            if n==5:
                break
    else:
        print("Incorrect password")
        
         
    
import os.path
import random
import time
import json
#from tabulate import tabulate

import os.path
import random
import time
import json

def replace_equipment():
    # Load user and equipment data
    if os.path.isfile("user_data.json") is False:
        user_data = {}
    else:
        with open("user_data.json", 'r') as fd:
            txt = fd.read()
            user_data = json.loads(txt)
            
    with open("Eq_data.json", 'r') as fd:
        txt = fd.read()
        Eq_data = json.loads(txt)
        
    # Input user ID
    print("Enter your user ID:")
    user_id = input().strip()
    
    # Check if user exists
    if user_id not in user_data:
        print("User ID doesn't exist.")
        return
    
    # Display user's equipment
    print("Your equipment:")
    for item_id, item_info in user_data[user_id].items():
        print(f"ID: {item_id}, Equipment: {item_info['Equipment_name']}, Quantity: {item_info['Quantity']}")
    
    # Input item ID for replacement
    print("Enter the ID of the equipment you want to replace:")
    item_id_to_replace = input().strip()
    
    # Check if item ID is valid
    if item_id_to_replace not in user_data[user_id]:
        print("Invalid item ID.")
        return
    
    # Input new item ID
    print("Enter the ID of the new equipment:")
    new_item_id = input().strip()
    
    # Check if new item ID is valid
    if new_item_id not in Eq_data:
        print("Invalid new item ID.")
        return
    
    # Replace equipment
    old_equipment_info = user_data[user_id][item_id_to_replace]
    new_equipment_info = Eq_data[new_item_id]
    user_data[user_id][item_id_to_replace] = {
        'tDate': str(time.ctime()),
        
        'Equipment_name': new_equipment_info['Equipment_name'],
        'Category': new_equipment_info['Category'],
        'Quantity': old_equipment_info['Quantity'],  # Maintain old quantity
        'Price': new_equipment_info['Price'],
        'Transaction ID': ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(10))
    }
    
    # Update equipment quantity in Eq_data
    Eq_data[new_item_id]['Quantity'] = str(int(Eq_data[new_item_id]['Quantity']) - int(old_equipment_info['Quantity']))
    
    # Save updated data to files
    with open("Eq_data.json", 'w') as fd:
        js = json.dumps(Eq_data)
        fd.write(js)
        
    with open("user_data.json", 'w') as fd:
        js = json.dumps(user_data)
        fd.write(js)
    
    # Store replaced equipment information in a separate file
    replaced_equipment_info = {
        'User_ID': user_id,
        'Replaced_Equipment': {
            'Old_Equipment': old_equipment_info,
            'New_Equipment': new_equipment_info
        }
    }
    with open("replaced_equipment.json", 'a') as fd:
        js = json.dumps(replaced_equipment_info)
        fd.write(js)
        fd.write('\n')
        
    # Display replaced equipment info
    print("\nReplaced Equipment Information:")
    print("+----------------------+")
    print("| {:<20} |".format("User ID: " + replaced_equipment_info['User_ID']))
    print("| {:<20} |".format("Old Equipment ID: " + item_id_to_replace))
    print("| {:<20} |".format("Old Equipment Name: " + old_equipment_info['Equipment_name']))
    print("| {:<20} |".format("New Equipment ID: " + new_item_id))
    print("| {:<20} |".format("New Equipment Name: " + new_equipment_info['Equipment_name']))
    print("+----------------------+")
    
    print("\nEquipment replacement successful.")
    print("Thank you for using our service!")

#replace_equipment()

#replace_equipment()

# Example usage:
#replace_equipment()

    


def user():
    print("WELCOME TO USER ATHLETIC EQUIPMENT INVENTORY SYSTEM ")
    while(1):
        print("1:Display equipments")
        print("2:collect equipments")
        print("3:Request for replacements")
        print("4:Exit")
        print("Enter your choice")
        n=int(input())
        if n==1:
            display_data()
        if n==2:
            collect_equipment()
        if n==3:
            replace_equipment()
        if n==4:
            break
def display_data():
    import pandas as pd
    import json
    fd=open("Eq_data.json",'r')
    txt=fd.read()
    Eq_data=json.loads(txt)
    fd.close()
    table=pd.DataFrame(columns=['Equipment_name','Category','Price','Quantity','Date'])
    for i in Eq_data.keys():
        temp=pd.DataFrame(columns=['ID']) 
        temp['ID']=[i]
        for j in Eq_data[i].keys():
            temp[j]=[Eq_data[i][j]]
        table=table._append(temp)
    table=table.reset_index(drop=True)
    from IPython.display import display
    display(table)
#display_data()
def insert_equipments():
    import json
    fd = open("Eq_data.json", 'r')
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    print("Enter New Equipment ID :- ")
    id = input()
     
    if id not in data.keys():
        print("Enter equipment name:- ")
        equipment = input()
         
        print("Enter Category  :- ")
        category  = input()
         
        print("Enter price :- ")
        price = input()
         
        print("Enter Quantity of Product :- ")
        quantity = input()
         
        print("Enter The Date on Which Product is Added in Inventory :- ")
        date = input()
         
        data[id] = {'Equipment_name':equipment ,'ID':id, 'Price': price,
                    'Category': category, 'Quantity': quantity, 'Date': date}
    else:
        print("Equipment ID is already available")
       
    js = json.dumps(data)
    fd = open("Eq_data.json", 'w')
    fd.write(js)
    fd.close()
    #insert_equipments()
    #display_data()
def delete_equipments():
    import json
    fd = open("Eq_data.json", 'r')
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    print("Enter The Equipment ID of The Product Which You Want To Delete :- ")
    temp = input()
     
    if temp in data.keys():
       
          # here we are removing that particular data
        data.pop(temp)  
        print("-------Equipment ID "+str(temp)+" Deleted Successfully...!!!--------")
    else:
        print("Invalid Equipment ID...!!!")
    js = json.dumps(data)
    fd = open("Eq_data.json", 'w')
    fd.write(js)
    fd.close()
    #delete_equipments()
    #display_data()
def display_user_reports():
	import pandas as pd
	import json
	if (os.path.isfile("user_data.json") is False):
		# Check if the file is present or not
		# The file will be generated only if any user makes a purchase
		print("No User Reports are Present")
		return
	fd = open("user_data.json", 'r')
	txt = fd.read()
	user_data = json.loads(txt)
	fd.close()
	print("Enter '0' to Check All Bills/Reports and '1' To Check Specific User Bills/Reports: ")
	n = int(input())
	if (n == 1):
		print("Enter User ID Whose Details You Want to Have a Look on:")
		user_id = input()
		temp = pd.DataFrame()
		if user_id in user_data.keys():
			for purchase_number, purchase_info in user_data[user_id].items():
				report = {'User ID': user_id, 'Purchase Number': purchase_number}
				for key, value in purchase_info.items():
					if key == 'pID':
						report['ID'] = value if value else 'N/A'  # Include Equipment ID if available, otherwise 'N/A'
					else:
						report[key] = value
				temp = temp.append(report, ignore_index=True)
			temp = temp.reset_index(drop=True)
			from IPython.display import display
			display(temp)
		else:
			print("The entered User ID does not exist in the database.")
	elif (n == 0):
		table = pd.DataFrame()
		for user_id, purchases in user_data.items():
			for purchase_number, purchase_info in purchases.items():
				report = {'User ID': user_id, 'Purchase Number': purchase_number}
				for key, value in purchase_info.items():
					if key == 'pID':
						report['Equipment ID'] = value if value else 'N/A'  # Include Equipment ID if available, otherwise 'N/A'
					else:
						report[key] = value
				table = table._append(report, ignore_index=True)
		table = table.reset_index(drop=True)
		from IPython.display import display
		display(table)
	else:
		print("Please enter a valid choice.")

# Example usage:
# display_user_reports()

        
'''js=json.dumps(available_equipments)
fd=open("Eq_data.json",'w')
fd.write(js)
fd.close()'''

def generate_bill(user_id, prod_id, price, time_date, purchase_no, 
				name, category, quantity_all, transaction_id):
	print("========= Bill ========")
	print("#######################")
	print(" User ID :-", user_id)
	print("#################")
	amount = 0
	n = len(purchase_no)
	
	for i in range(n):
		print("-----------------------------------------")
		amount = amount+float(price[i])*float(quantity_all[i])
		print("Purchase number", purchase_no[i],
			"\nPurchase Time :-", time_date[i], "\nProduct ID :-", 
			prod_id[i], "\nName Of Product :-",
			name[i], "\nCategory Of Product :-", category[i],
			"\nPrice of Product per Item :-", price[i],
            "\nReturn Date=",datetime.date.today()+timedelta(days=10),
			"\nPurchase Quantity :-", quantity_all[i])
		print("-----------------------------------")
	print("*")
	print(" Total Payable Bill :-",
		amount, "Transaction ID :-", transaction_id)
	print("*")
def collect_equipment():
    import os.path
    import random
    import time
    import json
    if os.path.isfile("user_data.json")is False:
        user_data={}
    else:
        fd=open("user_data.json",'r')
        txt=fd.read()
        user_data= json.loads(txt)
        fd.close()
    fd=open("Eq_data.json",'r')
    txt=fd.read()
    Eq_data=json.loads(txt)
    fd.close()
    print("Enter your user ID if your ID exists else press 0 to new user ID :-")
    p=int(input())
    if p==0:
        if len(user_data.keys())==0:
            user_id= 1123
        else:
            user_id=int(list(user_data.keys())[-1])+1    
    else:
        if str(p) in user_data.keys():
            user_id=p
        else:
            user_id=-1
    if user_id!=-1:
        user_id=str(user_id)
        Price=[]
        tDate=[]
        Collecting_no=[]
        Equipment_name=[]
        Category=[]
        Quantity_all=[]
        pID=[]
        o="0123456789abcdefghijklmnopqrstuvwxyz"
        transaction_id=''.join(random.choice(o)for i in range(10))
        print("Enter the number of products you want to buy :-")
        n=int(input())
        print("Enter Data As Follows :- ")
         
        if user_id not in user_data.keys():
            user_data[user_id] = {}
            g = 0
        else:
            g = int(list(user_data[user_id].keys())[-1])+1     
        for i in range(n):
            print("Enter Equipment ID of Product " +
                  str(i+1)+" that you want to buy")
            ID = input()
            if ID in Eq_data.keys():
                user_data[user_id][str(i+1+g)] = {}
                user_data[user_id][str(i+1+g)]['tDate'] = str(time.ctime())
                tDate.append(str(time.ctime()))
                if(float(Eq_data[ID]['Quantity']) == 0):
                    print("Product You Want is Currently Out Of Stock...!!!")
                    continue
                Collecting_no.append(i+1+g)
                Equipment_name.append(Eq_data[ID]['Equipment_name'])
                user_data[user_id][str(i+1+g)]['Equipment_name'] = Eq_data[ID]['Equipment_name']
                pID.append(ID)
                user_data[user_id][str(i+1+g)]['pID'] = ID
                Category.append(Eq_data[ID]['Category'])
                user_data[user_id][str(
                    i+1+g)]['Category'] = Eq_data[ID]['Category']
                print("For Product "+str(Eq_data[ID]['Equipment_name']) +
                      " Available Quantity is :- "+str(Eq_data[ID]['Quantity']))
                print("Enter Quantity of Product " +
                      str(i+1)+" that you want to buy")
                Quantity = input()
                 
                if (float(Quantity) <= float(Eq_data[ID]['Quantity'])):
                    Eq_data[ID]['Quantity'] = str(
                        float(Eq_data[ID]['Quantity'])-float(Quantity))
                    Quantity_all.append(Quantity)
                    user_data[user_id][str(i+1+g)]['Quantity'] = str(Quantity)
                    Price.append(Eq_data[ID]['Price'])
                    user_data[user_id][str(i+1+g)]['Price'] = Eq_data[ID]['Price']
                    user_data[user_id][str(
                        i+1+g)]['Transaction ID'] = str(transaction_id)
                else:
                    print(
                        "The Quantity You Have Asked is Quite High\
                        Than That is Available in Stock")
                    print(
                        "Did you Want To buy According to The Quantity\
                        Available in Stock then Enter '0' Else '1'\
                        to skip This Product")
                    key = int(input())
                     
                    if (key == 0):
                        print("Enter Quantity of Product " +
                              str(i+1)+" that you want to buy")
                        Quantity = input()
                        if (float(Quantity) <= float(Eq_data[ID]['Quantity'])):
                            Eq_data[ID]['Quantity'] = str(
                                float(Eq_data[ID]['Quantity'])-float(Quantity))
                            Quantity_all.append(Quantity)
                            user_data[user_id][str(
                                i+1)]['Quantity'] = str(Quantity)
                            Price.append(Eq_data[ID]['Price'])
                            user_data[user_id][str(
                                i+1)]['Price'] = Eq_data[ID]['Price']
                            user_data[user_id][str(
                                i+1+g)]['Transaction ID'] = str(transaction_id)
                        else:
                            print("Invalid Operation Got Repeated...!!!")
                    elif (key == 1):
                        continue
                    else:
                        print("Invalid Choice...!!!")
            else:
                print("Invalid Equipment ID...!!!")
        if(len(Collecting_no) != 0):
            generate_bill(user_id, pID, Price, tDate, Collecting_no,
                          Equipment_name, Category, Quantity_all, transaction_id)
    else:
        print("User ID Doesn't Exists...!!!")
    js = json.dumps(Eq_data)
    fd = open("Eq_data.json", 'w')
    fd.write(js)
    fd.close()
    js = json.dumps(user_data)
    fd = open("user_data.json", 'w')
    fd.write(js)
    fd.close()
while(1):
    print("Choose any one of the following")
    print("1:Admin")
    print("2:user")
    print("3:Exit")
    print("Enter your choice")
    n=int(input())
    if n==1:
        admin()
    if n==2:
        user()
    if n==3:
        break