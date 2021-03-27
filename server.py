import json
from subProcessHandler import SubProcessHandler
import socket
import sys

HTTPResponseSuccessHdr = '''
HTTP/1.x 200 ok
Content-Type: text/html
'''

HTTPResponseFailedHdr = '''
HTTP/1.x 500 internal server error
Content-Type: text/html
'''

def runServer(host, port, spHandler):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(100)

	while True:
		connection, address = sock.accept()
		requestData = connection.recv(1024).decode('utf-8')
		requestMethod = requestData.split(' ')[0]
		requestRoute = requestData.split(' ')[1]
		print("request data:", requestData)

		if requestMethod == 'GET':
			if requestRoute	 == '/favicon.ico':
				continue
			elif requestRoute == '/off':
				handlerResult = spHandler.terminateProcess()
				if spHandler.isActionSuccess():
					HTTPResponseContent = HTTPResponseSuccessHdr + makeResponseBody('off', True)
				else:
					HTTPResponseContent = HTTPResponseFailedHdr + makeResponseBody('off', False)
			else:
				spHandler.createProcess(requestRoute[1:])
				if spHandler.isActionSuccess():
					HTTPResponseContent = HTTPResponseSuccessHdr + makeResponseBody(requestRoute[1:], True)
				else:
					HTTPResponseContent = HTTPResponseFailedHdr + makeResponseBody(requestRoute[1:], False)
		else:
			HTTPResponseContent = HTTPResponseFailedHdr
		print("send data:", HTTPResponseContent)
		connection.sendall(HTTPResponseContent.encode('utf-8'))
		connection.close()

#		if requestMethod == 'GET':
#			if requestRoute == '/test':
#				content = response_hdr + 'test\n'
#			elif requestRoute == '/off':
#				content = response_hdr + off(spHandler)
#			elif requestRoute == '/white':
#				content = response_hdr + white(spHandler)
#			elif requestRoute == '/clock':
#				content = response_hdr + clock(spHandler)
#			elif requestRoute == '/rainbow':
#				content = response_hdr + rainbow(spHandler)
#			else:
#				continue
#		else:
#			continue
#		connection.sendall(content.encode('utf-8'))
#		connection.close()



def makeResponseBody(command, result):
	if result:
		return json.dumps({'status': command, 'result': 0})
	else:
		return json.dumps({'status': command, 'result': 1})

#def off(spHandler):
#	try:
#		spHandler.terminateProcess()
#		return response('off', True)
#	except Exception as e:
#		print(e)
#		return response('off', False)

#def white(spHandler):
#	try:
#		spHandler.createProcess('white')
#		return reponse('white', True)
#	except Exception as e:
#		print(e)
#		return response('white', False)

#def clock(spHandler):
#	try:
#		spHandler.createProcess('clock')
#		return response('clock', True)
#	except Exception as e:
#		print(e)
#		return response('clock', False)
#
#def rainbow(spHandler):
#	try:
#		spHandler.createProcess('rainbow')
#		return response('rainbow', True)
#	except Exception as e:
#		print(e)
#		return response('rainbow', False)

#def rainbow2(spHandler):
#	try:
#		spHandler.createProcess('rainbow2')
#		return response('rainbow2', True)
#	except Exception as e:
#		print(e)
#		return response('rainbow2', False)

if __name__ == '__main__':
	if len(sys.argv) == 2 and int(sys.argv[1]) > 1024 and int(sys.argv[1]) < 65536:
		port = int(sys.argv[1])
		spHandler = SubProcessHandler()
		if spHandler.isActionSuccess():
			runServer('', port, spHandler)
		else:
			print("config error")
	else:
		print("argument incorrect")
	
