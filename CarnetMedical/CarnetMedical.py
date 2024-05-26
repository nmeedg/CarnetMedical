class CarnetMedical:
    def __init__(self, infos, liste_page:list):
        self.infos = infos
        self.liste_page = liste_page



class Information_Patient:
    def __init__(self,nom:str, prenom:str, sexe:str, age:int, quartier:str,ville:str, groupe_sanguin:str,
                 rhesus:str,liste_allergies:list,liste_maladies_actuelles:list,
                 numeros:list, numeros_urgence:list,situation_particuliere:list,mot_de_passe):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.sexe = sexe
        self.quartier = quartier
        self.ville = ville
        self.groupe_sanguin = groupe_sanguin
        self.rhesus = rhesus
        self.liste_allergies = liste_allergies
        self.liste_maladies_actuelles = liste_maladies_actuelles
        self.numeros = numeros
        self.numeros_urgence = numeros_urgence
        self.situation_particuliere = situation_particuliere
        self.mot_de_passe = mot_de_passe




class PageCarnetMedical :
    def __init__(self,observation,examen,conclusion,posologie,image):
        pass