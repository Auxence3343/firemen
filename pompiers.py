# Nicolas, appelle moi si tu as des questions ( Auxence )
from map import *


class Pompier:
    def __init__(self, pos_x, pos_y, pv):
        """ cree un pompier (a completer)"""
        self.x = pos_x
        self.y = pos_y
        self.points_de_vie = pv
        self.chemin_a_suivre = []  # liste des cases par lesquelles le pompier veut passer

    def avancer_d_une_case(self):
        """ le pompier se 'teleporte' a la prochaine case de sa liste ( a faire )
        /!\ avant d'utiliser cette methode il faut verifier que la case en question est vide /!\
        /!\ la methode devra effacer la case de la liste ou le pompier s'est deplace
        """
    def trouver_un_chemin(self, x_cible, y_cible, cases_a_eviter):
        """ ( a faire ) trouve un chemin entre la position actuelle et la position_cible puis met ce chemin dans
        la liste 'chemin_a_suivre' a la place du chemin existant. l'ideal serait d'utiliser l'algo A* mais commence
        en faisant simple avec un algo qui va juste choisir la case adjacente a sa position qui ne brule pas,
        qui n'est pas dans la liste des cases interdites et qui est la plus proche de la cible jusqu'a atteindre
        cette dernière
        
        PS : va checker ma méthode infos_sur_la_case de la classe matrice, elle va t'aider a connaitre
        l'etat d'une case"""


class ToutLesPompiers:
    def __init__(self, matrice):
        self.pompiers = []  # liste de touts les pompiers existants
        self.matrice = matrice  # la classe 'matrice' dans laquelle les pompiers évoluent

    def ajouter_pompier(self, x, y):
        """ cree un pompier et l'ajoute dans la liste (a faire)"""
