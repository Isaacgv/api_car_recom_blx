import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

# Basic Authentication with Watson STT API
    
stt_authenticator = BasicAuthenticator(
        'apikey',
        'yH2qmAtMsfapTdFSh12-MgcGoZ9z17SC-rFfY5VCaenz'
)

# Construct a Watson STT client with the authentication object
stt = SpeechToTextV1(
        authenticator=stt_authenticator
    )

# Set the URL endpoint for your Watson STT client
stt.set_service_url(
        'https://api.us-south.speech-to-text.watson.cloud.ibm.com'
)


def recive_audio(audio_file_):

    with open(join(dirname(__file__), audio_file_),
              'rb') as audio_file:
        #audio_source = AudioSource(audio_file)
        stt_result = stt.recognize(
            audio=audio_file,
            content_type='audio/flac',
            model='pt-BR_BroadbandModel',
	    ).get_result()
    #pt-BR_NarrowbandModel
    #print(json.dumps(stt_result, indent=2))

    text_tr = stt_result['results'][0]['alternatives'][0]['transcript']
    
    return text_tr
