from flask import Flask, request, send_file, jsonify
import ffmpeg
import os
import string, random

app = Flask(__name__)

def convert_m3u8_to_mp4(m3u8_url, output_filename):
    # Utilisation de ffmpeg pour convertir le fichier m3u8 en mp4
    process = (
        ffmpeg
        .input(m3u8_url)
        .output(output_filename, codec='copy')
        .run()
    )

    
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        data = request.json
        m3u8_url = data.get('m3u8_url')
    else:
        m3u8_url = request.args.get('m3u8_url')
    
    if not m3u8_url:
        return jsonify({"error": "m3u8_url is required"}), 400

    output_filename = randomword(10) + "outputvid.mp4"
    
    try:
        convert_m3u8_to_mp4(m3u8_url, output_filename)
        #return jsonify({"ok": "k"}), 400
        # Envoyer le fichier MP4 en tant que réponse
        return send_file(output_filename, mimetype='video/mp4', as_attachment=True, download_name='output.mp4')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Supprimer le fichier temporaire après l'envoi
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25572)
