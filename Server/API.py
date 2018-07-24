from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import base64

import BufferManagement
import os

from json import dumps
import json

app = Flask(__name__)
api = Api(app)


class UserInfo(Resource):
    def get(self, UserID,GameID):
        return jsonify((UserID,GameID))

    def post(self, UserID,GameID):
        incoming = json.loads(request.data)
        print(incoming['image'])
        image = incoming['image']
        image = image.encode('utf-8')
        fh = open("imageToSave.png", "wb")
        fh.write(base64.b64decode(image))
        fh.close()

class KillPlz(Resource):
    def post(self, UserID,GameID):
        incoming = json.loads(request.data)
        BufferManagement.append_to_buffer(incoming, UserID, GameID, "IN")
        pass

class Vote1(Resource):
    def post(self,UserID,GameID):
        incoming = json.loads(request.data)
        BufferManagement.append_to_buffer(incoming, UserID, GameID, "IN")
        pass

class Vote2(Resource):
    def post(self,UserID,GameID,killImage):
        pass

class GetCommand(Resource):
    """Needs authentication/ method to endsure commands recieved correctly before being deleted"""
    def get(self,UserID,GameID):
        commands = BufferManagement.empty_buffer(GameID,UserID,"OUT")
        return(jsonify(commands))

class JoinGame(Resource):
    def post(self,UserID,GameID):
        incoming = json.loads(request.data)
        PlayerDetails = incoming
        if not os.path.isfile("IN"+GameID+'/'+ UserID +".pkl"):
            BufferManagement.create_buffer(UserID,GameID,"IN")
        if not os.path.isfile("OUT"+GameID+'/'+ UserID +".pkl"):
            BufferManagement.create_buffer(UserID,GameID,"OUT")
        BufferManagement.append_to_buffer(PlayerDetails,UserID,GameID,"IN")


api.add_resource(UserInfo, '/Info/<UserID>/<GameID>')  # Route_1
api.add_resource(KillPlz, '/Kill/<UserID>/<GameID>')  # Route_1
api.add_resource(Vote1, '/Vote1/<UserID>/<GameID>')  # Route_1
api.add_resource(Vote2, '/Vote2/<UserID>/<GameID>')  # Route_1
api.add_resource(GetCommand, '/GetCommand/<UserID>/<GameID>')  # Route_1
api.add_resource(JoinGame, '/JoinGame/<UserID>/<GameID>')  # Route_1

if __name__ == '__main__':
    app.run(port=5002)