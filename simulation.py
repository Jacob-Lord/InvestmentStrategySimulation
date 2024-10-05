import random
import time
from tabulate import tabulate

def init_rand_nums(num_list, n):
    '''
    Generates n amount of random float numbers and stores them in a list
    Parameters: num_list - empty list to store nums
                n - amount of numbers to generate
    Returns: list with n amount of random float values
    '''
    for i in range(n):
        time.sleep(0.1) #random() runs off of system time, so sleeping for a tenth of a second adds entropy to num_list
        rand_val = random.random()
        num_list.append(rand_val)

def stock_increase(stock_price, change_rate):
    price_change = stock_price * change_rate
    stock_price += price_change
    return stock_price
    
def stock_decrease(stock_price, change_rate):
    price_change = stock_price * change_rate
    stock_price -= price_change
    return stock_price

def simulate_stock_price_change(stock_price, rand_val, change_rate):
    if (rand_val < 0.5): #hold case
        #do nothing?
        #print('Did nothing for month ' + str(i))
        x = 5
    elif (rand_val >= 0.5 and rand_val < 0.75): #stock decrease case
        #stock decreased in value
        stock_price = stock_decrease(stock_price, change_rate)

    elif (rand_val >= 0.75 and rand_val < 1): #stock increase case
        #stock increased in value
        stock_price = stock_increase(stock_price, change_rate)
        
    else: #somehow got a number outside of [0, 1) range
        print("Error un-uniform distribution??")
        exit(1)

    return stock_price

def buy_stock(bank_acct_amt, stock_amt, stock_price):
    stock_amt = bank_acct_amt / stock_price #calculate amount of stock that can be purchased and "purchase" it
    bank_acct_amt = 0 #set amount to 0 because we bought stock with it
    return bank_acct_amt, stock_amt

def sell_stock(bank_acct_amt, stock_amt, stock_price):
    bank_acct_amt = stock_amt * stock_price #calculate how much the stock is worth and "sell" it
    stock_amt = 0 #set stock amount to 0 because we sold it
    return bank_acct_amt, stock_amt

def main():
    random_num_list = [] #declare list to hold randomly generated numbers
    results_table = [] #table to store results of simulation every month
    bank_acct_amt = 1000 #initial investment amount
    months = 60 #number of months to simulate; 5 years in this case
    stock_price = 100 #initial stock price
    interest_amt = 0 #amount of interest made from savings 
    interest_rate = 0.005 #interest rate of savings account if money is held in there
    change_rate = 0.05 #rate of change for stock every month if it changes
    buy_limit = 95 #boundary point where we choose to convert our money to stock
    sell_limit = 110 #boundary point where we choose to sell our stock for money
    stock_amt = 0 #amount of stock held by user
    table_headers = ["Month", "Random Value", "New Stock Price", "Action", "Number of Stocks", "Worth", "Bank Balance", "Interest Amount", "New Bank Balance"] #explicit headers for the table output of simulation results
    action = "Hold" #action taken by user

    init_rand_nums(random_num_list, months) #initialize random number list with 60 randomly generated numbers to represent 60 months (5 years)

    for i in range(months):
        rand_val = random_num_list[i]

        stock_price = simulate_stock_price_change(stock_price, rand_val, change_rate)

        #condition to buy stock
        if (stock_price < buy_limit and bank_acct_amt > 0):
            bank_acct_amt, stock_amt = buy_stock(bank_acct_amt, stock_amt, stock_price) #call buy stock function
            action = "Buy"
        #condition to sell stock for money
        elif (stock_price > sell_limit and stock_amt > 0):
            bank_acct_amt, stock_amt = sell_stock(bank_acct_amt, stock_amt, stock_price) #call sell stock function
            action = "Sell"
        #default condition where assets are held
        else:
            action = "Hold"
        
        #calculate interest and bank account information
        interest_amt = bank_acct_amt * interest_rate #calculate amount gained from interest
        old_bank_acct_amt = bank_acct_amt #track amount before savings interest is applied
        bank_acct_amt += interest_amt #add interest amount to savings account

        #calculate worth of stock every iteration
        stock_worth = stock_amt * stock_price 
        
        #track simulation results in 2D table
        results_table.append([i+1, rand_val, stock_price, action, stock_amt, stock_worth, old_bank_acct_amt, interest_amt, bank_acct_amt])

    #tabulate() converts the results table  list into a table format and puts the defined header values at the top
    results_tabulated = tabulate(results_table, headers = table_headers)
    print(results_tabulated)

main() #run simulation program
