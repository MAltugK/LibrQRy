from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

qr_message = ""

@app.route('/userscanner', methods=['GET'])
def userscanner():
    return render_template('userscanner.html')

@app.route('/managerscanner', methods=['GET'])
def managerscanner():
    return render_template('managerscanner.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/qr-okundu-user', methods=['POST'])
def qr_okundu_user():
    global qr_message
    data = request.json
    if 'qr_content' in data:
        qr_content = data['qr_content']
        print(f"QR Okundu: {qr_content}")
        if int(qr_content) >= 0 and int(qr_content) < 15:
            greentored_file_editor(qr_content)
        qr_message = qr_content
        return jsonify({"message": "OK"})
    else:
        return jsonify({"error": "HATA: QR içeriği bulunamadı!"}), 400

@app.route('/qr-okundu-manager', methods=['POST'])
def qr_okundu_manager():
    global qr_message
    data = request.json
    if 'qr_content' in data:
        qr_content = data['qr_content']
        print(f"QR Okundu: {qr_content}")
        if int(qr_content) >= 0 and int(qr_content) < 15:
            redtoyellow_file_editor(qr_content)
        qr_message = qr_content
        return jsonify({"message": "OK"})
    else:
        return jsonify({"error": "HATA: QR içeriği bulunamadı!"}), 400


@app.route('/qr-durum')
def qr_durum():
    global qr_message
    return jsonify({"qr_message": qr_message})

def greentored_file_editor(table):
    with open('templates/manager.html', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('<div class="redbox" id="id' + table + '"></div>', '<div class="greenbox" id="id' + table + '"></div>')

    # Write the file out again
    with open('templates/manager.html', 'w') as file:
        file.write(filedata)

def redtoyellow_file_editor(table):
    with open('templates/manager.html', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('<div class="greenbox" id="id' + table + '"></div>', '<div class="yellowbox" id="id' + table + '"></div>')

    # Write the file out again
    with open('templates/manager.html', 'w') as file:
        file.write(filedata)

if __name__ == '__main__':
    app.run(debug=True)
