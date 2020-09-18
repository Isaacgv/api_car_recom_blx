import os
from flask import Flask, request
from flask_cors import CORS
from speech import recive_audio
from nlu import sentiment_nlu
app=Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins": "*"}})

#{
#    'car': (string)
#    'text': (string)
#    'audio':(file)
#}


@app.route("/mutipart/form-data", methods=["POST"])
def index():
    if not request.json:   
        abort(400)

    body = request.get_json()
    car = body['car'].lower().split()
    print(body)

    if  'audio' in body:
        text_audio = recive_audio(body["audio"])
        recommend = sentiment_nlu(text_audio, car)
        print(text_audio)
        return recommend
        
        
    
    elif 'text' in body:
        recommend = sentiment_nlu(body['text'], car)
        print(body['text'])  
        return recommend 

    else:
        abort(400)

def main():
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
