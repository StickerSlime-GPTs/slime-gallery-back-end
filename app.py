from flask import Flask, request, jsonify, Response
import requests
from decouple import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://slime-gallery.vercel.app", "http://localhost:3000"])

api_key = config('API_KEY')

@app.route('/removebg', methods=['POST'])
def remove_background():
    try:
        image_file = request.files['image_file']
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': image_file},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )
        if response.status_code == requests.codes.ok:
            # 바이너리 형태의 이미지 데이터를 직접 반환
            return Response(response.content, mimetype='image/png')
        else:
            return jsonify({'success': False, 'error_message': 'Background removal failed', 'status_code': response.status_code})
    except Exception as e:
        return jsonify({'success': False, 'error_message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
