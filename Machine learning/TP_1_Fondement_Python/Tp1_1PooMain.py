from processing import processing

#Calcul de R en mode console
print("Bienvenue au calcul de R")
Q1 = input("Voulez-vous continuer?\n(Oui ou Nom)")
while(Q1 == "O" or Q1 == "oui" or Q1 == "o"):
    try: #Gestion de quelques exceptions
        N = int(input("Donnez la valeur limite de la liste\n"))
        if N <= 0 :
            raise Exception
    except ValueError:
        print("Veillez entrer un nombre entier")
    except Exception:
        print("Veillez entrer un nombre entier strictement positif")
    else:
        task1 = processing(N)
        print("Début d'un nouveau traitement ")

        task1.execute()
        print("Fin detraitement ")

        Q2 = input("Voulez-vous quitter? (O ou N)")
        if(Q2 == "oui" or Q2 == "O" or Q2 == 'o'):
            quit()
        else: continue
