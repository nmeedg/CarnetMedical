import requests



endpoint = 'http://127.0.0.1:8000/medecin/1/all_informations/'

data1 = {'conclusion': 'positif'}
data2 = {'id_patient':1}
data3 = {**data2, **data1}
reponse = requests.get(endpoint, json=data3)
data = reponse.json()
print(data)



data2 = {'observation': 'frequence cardiaque stable, pression arterielle :23 \n Doit faire du sport', 'conclusion':
         'maladie(s): paludisme, medicament: quartem adulte, paracetamol 500ml 2 matin deux soir pendant 3 jours'}

data = {'id': 1, 'traitement_actuels':'cancer du foie',
        'groupe_sanguin':'AB', 'rhesus':'+', 'drepanocythose':'AA', 'poids':65,
        'taille':180, 'maladies': 'cancer de fois, hemophilie', 'handicap':'aucun'}