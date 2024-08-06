from bottle import Bottle, run, static_file, request
import pyfirmata2

# --------------------------

# ARDUINO SERIAL COM -------
ARDUINO_PORT = 'COM3'

board = pyfirmata2.Arduino(ARDUINO_PORT)
print("Setting up the connection to the board ...")

# default sampling interval of 19ms
board.samplingOn()

# --------------------------

# BOTTLE -------------------
app = Bottle()
ROOT_TEMPLATES = "GUI/templates"

# --------------------------

# WEBPAGES -----------------
   
# - - Admin Panel - -
admin_filename = "admin.html"
admin_route = "/admin"

# Route to serve the HTML page
@app.route(admin_route)
def admin():
    return static_file(admin_filename, ROOT_TEMPLATES)

# Route to handle the AJAX request
@app.post('/toggle')
def toggle(): 
    data = request.json
    pin = data['pin']
    state = data['state']
    print(f"Pin {pin} is {state}")

    if (state == "LOW"):
        board.digital[int(pin)].write(0)
    elif (state == "HIGH"):
        board.digital[int(pin)].write(1)
    else:
        print("ERROR IN BOARD STATE CHANGE")

    return "OK"

# --------------------------

# MAIN ---------------------

if __name__ == '__main__':
    run(app, host='localhost', port=8080)