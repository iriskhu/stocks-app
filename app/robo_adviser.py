import csv
from dotenv import load_dotenv
import json ## reference: https://github.com/prof-rossetti/nyu-info-2335-201805/blob/master/notes/programming-languages/python/modules/json.md
import os ## reference: https://github.com/prof-rossetti/nyu-info-2335-201805/blob/master/notes/programming-languages/python/modules/os.md#accessing-environment-variables
import pdb ## pdb.set_trace() ... python debug function
import requests
import datetime

def parse_response(response_text): ## source (partial sample codes): https://github.com/s2t2/stocks-app-py-2018/blob/master/app/robo_adviser.py
    ## response_text can be either a raw JSON string or an already-converted dictionary

    if isinstance(response_text, str): ## checking to see if the datatype of "response_text" is string---if not, then:
        response_text = json.loads(response_text) ## converting the string to a dictionary.

    results = []
    time_series_daily = response_text["Time Series (Daily)"] ## which is a nested dictionary
    for trading_date in time_series_daily: ## using for loop to loop through the dictionary's top-level keys/attributes

        #print(trading_date)  ... for testing purpose

        prices = time_series_daily[trading_date] #> {'1. open': '101.0924', '2. high': '101.9500', '3. low': '100.5400', '4. close': '101.6300', '5. volume': '22165128'}
        result = {
            "date": trading_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        } ## creating a new dictionary to store initial prices
        results.append(result)
    return results


def write_prices_to_file(prices=[], filename="db/prices.csv"): ## "price" here refers to "results"
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for d in prices: ## a list of dictionaries
            row = {
                "timestamp": d["date"], ## change attribute name to match project requirements
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
                "volume": d["volume"]
            }
            writer.writerow(row)


if __name__ == '__main__': ## only execute if file invoked from the command-line, not when imported into other files, like tests---Prof.'s notes

    load_dotenv() ## loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'."
    print(api_key) ## this statement can test your environment variable setup

    ## CAPTURE USER INPUTS (SYMBOL) & VALIDATE SYMBOL & PREVENT WRONG REQUESTS:
    symbol = input("Please input a stock symbol (e.g. 'NFLX'): ")
    if symbol.isalpha() and len(symbol) >5: ## reference: https://www.tutorialspoint.com/python/string_isalpha.htm
        print("Oops, please check your symbol and try again---should be no more than 5 letters.")
        quit()

    try: ## try function allows us to handle errors---Prof.'s notes
        float(symbol)
        quit("Oops! Please check your symbol and try again---a non-numeric symbol is expected.")
    except ValueError as e: ## Exception is the most general class of error---Prof.'s notes
    ## or put a "pass" here, and leave the rest codes un-indented. That also works---in class workshop

        ## ASSEMBLE REQUEST URL (USING THE SYMBOL & THE API KEY): (see https://www.alphavantage.co/support/#api-key)
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
        ## the f" allows us to perform string interpolation, which is one strategy to join two strings together---Prof.'s notes
        ## alternatively: request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + api_key

        ## ISSUE "GET" REQUEST
        response = requests.get(request_url)

        ## VALIDATING THE RESPONSE VARIABLE ABOVE AND HANDLE ERRORS:
        if "Error Message" in response.text:
            print("REQUEST ERROR, CAN'T FIND THAT STOCK SYMBOL. PLEASE TRY AGAIN.")
            quit("Quit the program")

        else:
            ## EVOKING THE PARSE RESPONSE (AS LONG AS THERE ARE NO ERRORS)
            print("------------------------------")
            print("Thanks! Your symbol is valid.")
            print("Issuing a request, please wait:")
            daily_prices = parse_response(response.text) ## remember that "daily_prices" is a list of dictionaries

            ## WRITING TO CSV
            write_prices_to_file(prices=daily_prices, filename="db/prices.csv") #evoking the write_prices_to_file function, wrting the prices to "db/prices.csv".

            ## PERFORM CALCULATIONS
            print("------------------------------")
            print("Stock: " + str(symbol))

            Checkout_time = datetime.datetime.now()
            print ("Run at: " + str(Checkout_time.strftime("%I:%M %p on %A, %B %d, %Y")))

            print ("Latest data from: " + str(daily_prices[0]["date"]))

            latest_closing_price = daily_prices[0]["close"] ##>'363.8300' as of 06-12-2018
            latest_closing_price = float(latest_closing_price)
            latest_closing_price_used = "${0:,.2f}".format(latest_closing_price)
            print ("Latest closing price: " + str(latest_closing_price_used))

            daily_high = [] ## reference: from the groceries.py assignment.
            for d in daily_prices:
                daily_high.append(d["high"])
            daily_high = list(map(float, daily_high)) ## converting str to float---reference: https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
            #print (daily_high) ... for testing purpose
            print ("Maximum daily high price: $" + str(max(daily_high)))
            print ("Average daily high price: " + str("${0:,.2f}".format(sum(daily_high)/float(len(daily_high))))) ## finding average of a list---reference: https://stackoverflow.com/questions/9039961/finding-the-average-of-a-list?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

            daily_low = []
            for d in daily_prices:
                daily_low.append(d["low"])
            daily_low = list(map(float, daily_low))
            #print(daily_low) ... for testing purpose
            print ("Minimum daily low price: $" + str(min(daily_low)))
            print ("Average daily Low price: " + str("${0:,.2f}".format(sum(daily_low)/float(len(daily_low)))))


            ## PRODUCE FINAL RECOMMENDATION
            min_daily_low = min(daily_low)
            min_daily_low_percent = float(min_daily_low) * 1.2
            if latest_closing_price > min_daily_low_percent:
                print ("Latest closing price is less than 20% above its recent minimum daily low price. Recommendation: Do not buy this stock.")
            else:
                print ("Latest closing price is more than 20% above its recent minimum daily low price. Recommendation: Consider buying this stock.")
