import socket
import netifaces
from flask import Flask
from flask import request

app = Flask(__name__)

request_count=0

@app.route('/')
def hello():
    global request_count
    request_count += 1

    html = "<h1>Hello Python Flask!</h1>"
    html += "<hr>"

    html += "<p>"
    html += "A simple hello web app, in a docker image, "
    html += "using debian, python and flask!"
    html += "</p>"

    html += "<p>"
    html += "Hostname: " + socket.gethostname()
    html += "</p>"

    html += "<p>"
    html += "Requests: " + str(request_count) + "<br \>"
    html += "</p>"

    html += "<p>"
    html += "Headers: " + str(dict(request.headers)) + "<br \>"
    html += "</p>"

    html += "<p>"

    for interface in netifaces.interfaces():
        if interface in ['lo']:
            continue

        ifaddresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in ifaddresses:
            html += "Network Interface: " + str(interface) + "<br \>"
            for ifaddress_inet in ifaddresses[netifaces.AF_INET]:
                html += "--> IP Address: " + str(ifaddress_inet['addr']) + "<br \>"
                html += "--> Netmask: " + str(ifaddress_inet['netmask']) + "<br \>"


    html += "</p>"


    return html

@app.route('/test')
def test():
    html = "<h1>ALB request headers</h1>"
    html += "<hr>"

    html += "<p>"
    html += "x-amzn-oidc-accesstoken: " + str(request.headers.get('x-amzn-oidc-accesstoken')) + "<br \>"
    html += "</p>"

    html += "<p>"
    html += "x-amzn-oidc-identity: " + str(request.headers.get('x-amzn-oidc-identity')) + "<br \>"
    html += "</p>"

    html += "<p>"
    html += "x-amzn-oidc-data: " + str(request.headers.get('x-amzn-oidc-data')) + "<br \>"
    html += "</p>"

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
