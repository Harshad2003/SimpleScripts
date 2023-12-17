import requests
from bs4 import BeautifulSoup
from twilio.rest import Client 
from apscheduler.schedulers.blocking import BlockingScheduler

size = 13  #Change the Shoe size According to your need, Works only for shoe sizes more than 12.
pages = 5
available_brands = []
total_available_models = 0
available_models = []
for page in range(1,pages): 
    flipkart = requests.get(f'https://www.flipkart.com/search?q=basketball+shoes&p%5B%5D=facets.size_uk%255B%255D%3D{size}&page={page}')
    if(flipkart.status_code==200):
        soup = BeautifulSoup(flipkart.text,'html.parser')
        brands = soup.findAll('div', {'class':'_2WkVRV'})
        models = soup.find_all('a',{'class':'IRpwTa'})
        j = 0
        for i in models:
            if 'Basket' in i.text:
                total_available_models = total_available_models + 1
                available_models.append(i.text)
                if(brands[j].text not in available_brands):
                    available_brands.append(brands[j].text)
            j = j + 1
    if(total_available_models==0):
        break


account_sid = 'Your Twillio SID' 
auth_token = 'Your Twillio auth_token' 
client = Client(account_sid, auth_token) 
def send_msg_in_stock():
    if(total_available_models):
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=f'*{size} UK NOW AVAILABLE AT FLIPKART* \nBRANDS = {available_brands}',      
                                    to='whatsapp:YOUR NUMBER'#YOUR NUMBER 
                                ) 
    
        print("MESSAGE SENT")
def send_msg_out_of_stock():
    if(total_available_models==0):
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=f'*{size} UK NOT AVAILABLE AT FLIPKART*',      
                                    to='whatsapp:YOUR NUMBER'#YOUR NUMBER
                                ) 
    
        print("MESSAGE SENT")


send_msg_in_stock()
send_msg_out_of_stock()
scheduler = BlockingScheduler()

scheduler.add_job(send_msg_in_stock,'interval',hours=24)
scheduler.add_job(send_msg_out_of_stock,'interval',hours=48)

scheduler.start()
