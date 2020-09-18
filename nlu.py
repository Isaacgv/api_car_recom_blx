import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EntitiesOptions, SentimentOptions

authenticator = IAMAuthenticator('iK9pmLdTnix6rFtyk5QArL_YEJYBpI38Wu8cAbgsn7_F')
natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/5388c617-58f5-4c03-9e7a-d98ca28368d9')

recomendation_positive = {
            "recommendation": "",
            "entities": []
        }

entitie_priority = {"SEGURANCA":1, "CONSUMO":2, "DESEMPENHO":3, "MANUTENCAO":4, "CONFORTO":5, "DESIGN":6, "ACESSORIOS":7} 

def sentiment_nlu(text_nlu, car):

    response = natural_language_understanding.analyze(
        text=text_nlu,
        features=Features(sentiment=SentimentOptions(document=True), entities=EntitiesOptions(sentiment=True, model='cf29a194-a31a-4ba2-a7e1-86791f221366'))).get_result()

    print(json.dumps(response, indent=2))

    sentiment_text_label = response["sentiment"]["document"]["label"]
    sentiment_text_score = response["sentiment"]["document"]["score"]

    if sentiment_text_label == 'positive' and sentiment_text_score > 0.5:
        return recomendation_positive

    #neutral, positive
    else :
        entitie_score_negative = 0
        etitie_isNegative = False
        
        entities_negatives_result = []
        for entitie_result in response["entities"]:
            entitie_type = entitie_result["type"]
            entitie_score = entitie_result["sentiment"]["score"]
            entitie_label = entitie_result["sentiment"]["label"]
            entitie_text = entitie_result["text"]
        
            if entitie_label == 'negative' or entitie_score < 0 :

                etitie_isNegative = True
                dict_results_negative = dict()
                dict_results_negative["entity"] = entitie_type
                dict_results_negative["sentiment"] = entitie_score
                dict_results_negative["mention"] = entitie_text
                
                entities_negatives_result.append(dict_results_negative)

                if (entitie_score < entitie_score_negative) :
                    if  abs(entitie_score - entitie_score_negative) < 0.1:
                        if entitie_priority[entitie_type_negative] < entitie_priority[entitie_type]:
                             continue
                    else:
                        entitie_score_negative = entitie_score
                        entitie_type_negative = entitie_type
                        entitie_text_negative = entitie_text

    if etitie_isNegative:
        print( entities_negatives_result)
        if "toro" in car:
            car_recommend = "RENEGADE"
        elif "renegade" in car:
            car_recommend = "TORO"
        elif "ducato" in car:
            car_recommend = "FIORINO"
        elif "fiorino" in car:
            car_recommend = "DUCATO"
        elif "cronos" in car:
            if entitie_type_negative == "ACESSORIOS":
                car_recommend = "MAREA"
            elif entitie_type_negative == "CONFORTO":
                car_recommend = "LINEA"
            else:
                car_recommend = "ARGO"
        elif "500" in car:
            if entitie_type_negative == "DESIGN":
                car_recommend = "LINEA"
            else:
                car_recommend = "MAREA"
        elif "marea" in car:
            if entitie_type_negative == "ACESSORIOS" or entitie_type_negative == "MANUTENCAO":
                car_recommend = "CRONOS"
            elif entitie_type_negative == "CONSUMO" or entitie_type_negative == "DESEMPENHO":
                car_recommend = "FIAT 500"
            else:
                car_recommend = "LINEA"
        elif "LINEA" in car:
            if entitie_type_negative == "DESIGN":
                car_recommend = "ARGO"
            else:
                car_recommend = "MAREA"
        elif "ARGO" in car:
            if entitie_type_negative == "ACESSORIOS" or entitie_type_negative == "CONSUMO" or entitie_type_negative == "DESEMPENHO" :
                car_recommend = "MAREA"
            else:
                car_recommend = "CRONOS"

        recomendation = {
            "recommendation": car_recommend
        } 

        recomendation["entities"] = entities_negatives_result
        return recomendation

    else:
        return recomendation_positive


