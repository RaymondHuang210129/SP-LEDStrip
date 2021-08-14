import json
from subProcessHandler import SubProcessHandler
import socket
import sys
import pathlib
import os

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
		try:
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
		except Exception as e:
			print(e)


def makeResponseBody(command, result):
	if result:
		return json.dumps({'status': command, 'result': 0})
	else:
		return json.dumps({'status': command, 'result': 1})

if __name__ == '__main__':
	filePath = pathlib.Path(__file__).parent.absolute()
	os.chdir(filePath)
	if len(sys.argv) == 2 and int(sys.argv[1]) > 1024 and int(sys.argv[1]) < 65536:
		port = int(sys.argv[1])
		spHandler = SubProcessHandler()
		if spHandler.isActionSuccess():
			runServer('', port, spHandler)
		else:
			print("config error")
	else:
		print("argument incorrect")
	
