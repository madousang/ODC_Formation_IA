from numpy import arctan
class processing:
    def __init__(self, limitePlage = 0):
        self.N = int(limitePlage)
        self.L = list()

    #Definition de la fonction f(x)
    def funct1(x):
        return (x/(x**2 + 1))
    
    #Definition de la fonction g(x)
    def funct2(y):
        return arctan(y)

    #Fonction pour générer la liste L et calcul de R
    def execute(self):
        deb = -1 * self.N
        fin = self.N + 1
        for i in range(deb, fin, 1):
            self.L.append(i)

        sum = 0
        for i in self.L:
            sum += (processing.funct1(i) - processing.funct2(i))**2
        print(round(sum, 2))
