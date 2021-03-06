import json
from app import *
from app.Models import *
from app.auth.admin_auth.utilis import admin_Required
from flask.views import MethodView
from flask import Blueprint, Flask, jsonify, make_response, request, current_app

menu = Blueprint('menu', __name__)

@swag_from('apidocs/getMenu.yaml', methods=['GET'])
def getmenu():   
    try:
        getMenuList = Admin.getCurrentMenu()
        changeToStr = str(getMenuList)
        changeToPyObject = json.loads(changeToStr)
        return jsonify(changeToPyObject)
        
    except:
        response={
            "Message":"Failed to get Menu"
        }
        return make_response(jsonify(response)), 500

class PostingToMenu(MethodView):
    decorators=[admin_Required]
    @swag_from('apidocs/postToMenu.yaml', methods=['POST'])
    def post(self):
        token=request.args.get('token')
        try:
            checkToken=BlacklistToken.query.filter_by(Token=token).first()
            if token==checkToken.Token:
                response={
                "Message":"You have an Expired Token, Login To get New Token."
                    }
                return make_response(jsonify(response)), 401
        
        except:
            try:
                request_data = request.get_json(force=True)
                Admin.addItemToMenu(request_data["Name"], request_data['Price'])
                response={
                    "Message":"Item has been added to Menu"
                }
                return make_response(jsonify(response)), 201
            
            except:
                response={
                    "Message":"Item has not been added to Menu"
                }
                return make_response(jsonify(response)), 500

posting_to_menu=PostingToMenu.as_view('posting_to_menu')
menu.add_url_rule('/menu', view_func=getmenu, methods=['GET'])
menu.add_url_rule('/menu', view_func=posting_to_menu, methods=['POST'])