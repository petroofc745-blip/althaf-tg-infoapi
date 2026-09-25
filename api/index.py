import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def proxy_api():
  # Get parameters from the incoming request
  key = request.args.get('key', '')
  tgid = request.args.get('tgid', '')
  types = request.args.get('types', 'telegram')
  spell = request.args.get('spell', '')

  # Construct the original backend API URL
  backend_url = f'https://rtf-api-server.onrender.com/api?types={types}&key={key}&spell={spell}'
  if tgid:
    backend_url += f'&tgid={tgid}'

  try:
    # Fetch data from the original API
    response = requests.get(backend_url)
    data = response.json()

    # Remove original tags, credits, or developer info if present in the JSON response
    if isinstance(data, dict):
      keys_to_remove = [
          'credit',
          'credits',
          'tag',
          'tags',
          'developer',
          'owner',
          'author',
          'created_by',
      ]
      for k in keys_to_remove:
        if k in data:
          data.pop(k, None)

      # Add your custom developer signature
      data['developer'] = '@Your_father_786k'

    return jsonify(data)

  except Exception as e:
    return jsonify({
        'error': True,
        'message': str(e),
        'developer': '@Your_father_786k',
    })


# Fallback root route
@app.route('/', methods=['GET'])
def home():
  return jsonify(
      {
          'status': 'Online',
          'developer': '@Your_father_786k',
          'usage': '/api?key=YOUR_KEY&tgid=USER_ID',
      }
  )


if __name__ == '__main__':
  app.run(debug=True)
