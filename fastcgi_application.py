#! /usr/bin/env python 

import flup.server.fcgi as flups 

def application(environment, start_response):
    response = "just for test"
    length = len(response)
    start_response("200 OK",
        [("Content-Length", str(length))])
    return [response]

if __name__ == "__main__":
    flups.WSGIServer(application).run()

