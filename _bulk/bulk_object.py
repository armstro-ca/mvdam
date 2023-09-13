import base64
import time
import urllib3

class BulkObject:
    def __init__(self):
        self.bulk_requests = []

    def add_request(self, request):
        self.bulk_requests.append(request)

    def get_all_requests(self):
        return self.bulk_requests
    
    def get_bulk_body(self):
        bulk_requests = {}
        boundary_string = base64.b64encode(
                bytes(f'MediaValetCLI bulk request initiated @ {time.time()}', 'utf-8"')
                ).decode("utf-8")
        
        boundary_string = 'c6c2ed020aadd284efd61a7c9d4dfe94'
        
        bulk_requests['headers'] = {'Content-Type': f'multipart/mixed; boundary={boundary_string}'}

        bulk_request_payloads = []

        for request in self.bulk_requests:
            bulk_request = ''.join(f'--{boundary_string}\r\n'
                                   'Content-Type: application/http; msgtype=request\r\n\r\n'
                                   f'{request["method"]} {request["uri"]} HTTP/1.1\r\n'
                                   f'host: {request["headers"]["Host"]}\r\n'
                                   f'Authorization: {request["headers"]["Authorization"]}\r\n'
                                   f'content-type: {request["headers"]["Content-Type"]}\r\n'
                                   )

            if request['data']:
                bulk_request += f'\r\n{request["data"]}\r\n'

            bulk_request_payloads.append(bulk_request)

        bulk_request_payloads.append(f'\r\n\r\n--{boundary_string}--')
        bulk_requests['payload'] = '\n'.join(bulk_request_payloads).encode(encoding='UTF-8', errors='strict')

        return bulk_requests
