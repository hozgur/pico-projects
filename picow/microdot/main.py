from time import sleep
from microdot import Microdot, send_file
from helpers import getFreeMemory, isPico
import grbl
if isPico():
    import wlan
    wlan.connect()

app = Microdot()

with open("index.html", "r", encoding = 'utf-8') as f:
    global indexHtml
    indexHtml = f.read()

def renderIndexPage():
    return indexHtml

@app.route('/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file(path)

@app.route('/')
def index(request):
    return renderIndexPage() , 200, {'Content-Type': 'text/html'}

@app.route('/command', methods=['POST'])
def command(request):
    print(request.form)
    command = request.form['command']
    grbl.sendCommand(command)
    return 'OK', 200


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

if grbl.connect():
    print("Grbl connected")
    app.run(debug=True)
else:
    print("Could not connect to grbl")