from requests_html import HTMLSession
import smtplib
import time

#Amazon Price Tracker
#This application checks Amazon and sends email notifications when an item's price drops below a given amount.

#method that runs the program
def runProgram():
    url = input("Enter an Amazon URL: ")
    price_floor = input("Enter a price floor (you will get an email if the item drops below this floor, do not include the dollar sign): ")
    price_floor_float = float(price_floor)
    email_address = input("Enter an email address where notifications will be sent: ")
    password = input("enter password for email: ")
    price = getPrice(url)
    if (price < price_floor_float):
        sendEmail(url, email_address, password)


#gets the price from Amazon given an Amazon URL
def getPrice(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)

    product = {
        'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
        'price': r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text
    }
    price = product.get('price')
    priceNoDollarSign = price[1:]
    print(product.get('title'))
    print(product.get('price'))
    return float(priceNoDollarSign)


#sends a notification email
def sendEmail(url, email, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, password)

    subject = 'Amazon Item Price Floor Reached'
    body = 'Your Amazon item has dropped below the specified price. Link to Item: ' + url

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(email, email, msg)
    print('Email Sent')
    server.quit()

#runs the program (updates price every day, frequency parameter can be changed below)
while(True):
    runProgram()
    time.sleep(86400)
