import random
import time

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
    bank_acct_amt = 1000 #initial investment amount
    months = 60 #number of months to simulate; 5 years in this case
    stock_price = 100 #initial stock price
    interest_amt = 0 #amount of interest made from savings 
    interest_rate = 0.005 #interest rate of savings account if money is held in there
    change_rate = 0.05 #rate of change for stock every month if it changes
    buy_limit = 95 #boundary point where we choose to convert our money to stock
    sell_limit = 110 #boundary point where we choose to sell our stock for money
    stock_amt = 0 #amount of stock held by user

    init_rand_nums(random_num_list, months) #initialize random number list with 60 randomly generated numbers to represent 60 months (5 years)

    for i in range(months):
        rand_val = random_num_list[i]

        stock_price = simulate_stock_price_change(stock_price, rand_val, change_rate)

        #condition to buy stock
        if (stock_price < buy_limit and bank_acct_amt > 0):
            bank_acct_amt, stock_amt = buy_stock(bank_acct_amt, stock_amt) #call buy stock function
        #condition to sell stock for money
        elif (stock_price > sell_limit and stock_amt > 0):
            bank_acct_amt, stock_amt = sell_stock(bank_acct_amt, stock_amt) #call sell stock function

        #if there is money in the savings account, apply interest rate to it and add the amount to the account.
        if (bank_acct_amt > 0): 
            interest_amt = bank_acct_amt * interest_rate #calculate amount gained from interest
            bank_acct_amt += interest_amt #add interest amount to savings account

        print("bank amt: " + str(bank_acct_amt) + " stock amt: " + str(stock_amt) + " stock price: " + str(stock_price))

main()
