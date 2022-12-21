class ExceptClass(Exception):
    def __init__(self, n):
        if (n<0): print("Le nombre de liste et la taille de chacune doivent etre >0")
        if (n == 0): print("Votre Liste ne contient-il aucun element????")
        