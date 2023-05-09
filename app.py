import qrcode
from io import BytesIO
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('home.html')\

@app.route('/capture_qr')
def capture_qr():
    return render_template('capture_qr.html')

@app.route('/gen_qr')
def formulario():
    return render_template('datos_personales.html')

@app.route('/api/qr', methods=['POST'])
def qr():
  data = request.get_json()
  qr_data = data.get('data')
  print(data)
  response_data = {'message': 'QR code detectado', 'data': qr_data}
  return response_data

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    nombre = request.form['nombre']
    ci = request.form['ci']
    placa = request.form['placa']
    telefono = request.form['telefono']

    if len(nombre) > 40:
        return 'El nombre no puede tener más de 40 caracteres'
    if not ci.isdigit() or len(ci) not in {11,6}:
        return 'El carnet de identidad debe tener 11 caracteres numéricos'
    if not placa.isalnum() or len(placa) != 7 or not placa[0].isalpha() or not placa[1:].isdigit():
        return 'La placa del carro debe tener una letra seguida de 6 dígitos'
    if not telefono.isdigit() or len(telefono) != 8:
        return 'El número de teléfono debe tener 8 caracteres numéricos'

    qr_text = f"Nombre: {nombre}\nCI: {ci}\nPlaca: {placa}\nTeléfono: {telefono}"

    # Generar el código QR
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_text)
    qr.make(fit=True)

    # Crear un objeto de BytesIO para guardar la imagen del código QR
    img_buffer = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_buffer, format='png')
    img_buffer.seek(0)

    # Enviar la imagen del código QR como respuesta
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
