from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from parse import search_query
import json

app = Flask(__name__)
CORS(app)
api = Api(app)


class search(Resource):
    def get(self, name):
        print(name)
        resp = {'result': [], 'time': ''}
        result, exe_time = search_query(name)
        print(exe_time)
        for index in range(len(result['body'])):
            resp['result'].append({
                'id': index,
                'url': result['url'][index],
                'title': result['title'][index],
                'body': result['body'][index],
            })
        resp['time'] = exe_time
        print(len(resp['result']))
        json.dumps(resp, indent=4, ensure_ascii=False)
        return resp


api.add_resource(search, '/api/search/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
