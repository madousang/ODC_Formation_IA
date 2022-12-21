#!/usr/bin/env python
# coding: utf-8

# In[7]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.errors import ParserError


csv_file_name = "scorm_tracking_copy.csv"


# In[ ]:





# In[11]:


class DataProcessing:
    
    #constructeur
    def __init__(self,chemin_fichier_csv,delimiter=";"):
        
        try :
            self.dataset = pd.read_csv(chemin_fichier_csv,delimiter=delimiter)
        except FileNotFoundError:
            print("Fichier nom trouver")
            
        except ParserError:
            print(f"Erreur de separateur '{delimiter}''")
        except :
            print("Une erreur s'est produite")
            
            
    
    def getListeColonne(self):
        return list(self.dataset)
    
    def regrouperSelon(self,col_list,agg_dic):
        _dataFrame = self.getDataset().groupby(col_list).agg(agg_dic)
        return _dataFrame
    
    
    def calculeTaux(self, trie=False, ascendant=True): # ici
        
        dataset_normaliser = (self.regrouperSelon(['object_id','actor'],{'score':'max'})).apply(self.__normalisation,axis='columns')
        
        nb_reussite = dataset_normaliser.groupby('object_id').agg({"score":"sum"})
        nb_total = dataset_normaliser.groupby('object_id').agg({"score":"size"})

        nb_total.rename({"score":"total"}, axis=1,inplace=True)

        #taux de reussite = (nb_de_reussite / nb_total) * 100
        df_taux_reussite = pd.DataFrame({"taux_de_reussite":round((nb_reussite.score / nb_total.total)*100,2)})

        
        if trie :
            df_taux_reussite.sort_values(['taux_de_reussite'],ascending=[ascendant],inplace=True)
            
        return df_taux_reussite
        
    
    def getStat(self):
        dataFrame_final = self.regrouperSelon(["object_id"],{"actor":['nunique'] ,"session_uuid":["count"],"score":["min",'max']})

        #Ajout du taux de reussite 
        df_taux_reussite = self.calculeTaux()
        dataFrame_final = pd.concat([dataFrame_final.actor,dataFrame_final.session_uuid,dataFrame_final.score,df_taux_reussite],axis=1)

        #renomage
        dataFrame_final.rename({"nunique":"nb_apprenants"}, axis=1,inplace=True)
        dataFrame_final.rename({"count":"nb_sessions"}, axis=1,inplace=True)
        dataFrame_final.rename({"min":"score_minimal"}, axis=1,inplace=True)
        dataFrame_final.rename({"max":"score_maximal"}, axis=1,inplace=True)


        # Trie par taux_de_reussite
        dataFrame_final.sort_values(['taux_de_reussite'],ascending=[False],inplace=True)

        return dataFrame_final
    
    
    def nTopModule(self,nombre, en_numpy=False):
        if en_numpy :
            return (self.getStat()).head(nombre).to_numpy()
        
        return (self.getStat()).head(nombre)
    
    def nLastModule(self,nombre, en_numpy=False):
        if en_numpy :
            return (self.getStat()).tail(nombre).to_numpy()
        return (self.getStat()).tail(nombre)
    
    def getDataset(self):
        return self.dataset
    
    
    def getModuleActorStat(self,nom_module):
        dataFrame_top_module = self.dataset.loc[self.dataset['object_id'] == nom_module].groupby('actor').agg({"session_uuid":['count'],"temps":['sum'],"score":['max']})
        dataFrame_top_module['resultat'] = 0 
        dataFrame_top_module.loc[dataFrame_top_module.score['max'] >= 50, 'resultat'] = 1

        dataFrame_top_module = pd.concat([dataFrame_top_module.session_uuid,dataFrame_top_module.temps,dataFrame_top_module.score,dataFrame_top_module.resultat],axis=1)

        dataFrame_top_module.rename({"count":"nb_sessions"}, axis=1,inplace=True)
        dataFrame_top_module.rename({"sum":"temps_total"}, axis=1,inplace=True)
        dataFrame_top_module.rename({"max":"score_max"}, axis=1,inplace=True)

        return dataFrame_top_module
    
    
    
    def courbeTempsFScoreMax(self,liste_module):
        
        module_index_liste = liste_module.index
        fig, ax = plt.subplots(figsize=(15, 5))

        for index in module_index_liste :
            x, y = self.__temps_et_score_from_object_id(index)
            ax.plot(x/60, y, label=index)
        #    

        ax.set_xlabel('temps (min)')
        ax.set_ylabel('score max')
        ax.legend();
        
        
    def diagrammeEnBaton(self,liste_module,horizontal=True):
        
        nom_des_module = np.array([name for name in liste_module.index])

        ordre_des_module = np.array([i for i in range(1,liste_module.index.size+1)])

        taux_de_reussite = np.array([t for t in liste_module.taux_de_reussite])


        if horizontal :
            plt.barh(nom_des_module,taux_de_reussite, color="cyan", height=0.5)  # horizontal
        else :
            plt.bar(ordre_des_module,taux_de_reussite) # Vertical
            for i in range(0,nom_des_module.size) :
                plt.annotate(nom_des_module[i], xy=(i+1, taux_de_reussite[i]), xytext=(i+1, len(liste_module)*3 + 120- i *5),
                         arrowprops=dict(facecolor='pink', shrink=0.01))

                
        plt.show()
        
    def courbeRangApprenantFScoreMax(self,liste_module):

        if len(liste_module) != 1 :
            fig, axs = plt.subplots(nrows=len(liste_module), ncols=1, figsize=(5, len(liste_module)*1.5+5),
                           gridspec_kw={'hspace': 0.4})
        else :
            fig, axs = plt.subplots()
            axs = [axs]
            
        for i in range(len(liste_module)) :  
            x ,y = self.__get_rang_score_max_by_module_name(liste_module.index[i])
            axs[i].plot(x,y);
            axs[i].set_title(liste_module.index[i])
            axs[i].set_ylabel('Score max')
            


    def nuagePoint(self,nom_colonne=['object_id'],agg_dic={'temps':'sum'},x_colonne='taux_de_reussite'):
        agg_data_sur_le_module = self.dataset.groupby(nom_colonne).agg(agg_dic)
        
        agg_dic_key = list(agg_dic.keys())[0]
        agg_dic_value = agg_dic[agg_dic_key]
        
        agg_data_sur_le_module = agg_data_sur_le_module[agg_dic_key]

        
        all_x_colonne_data = self.getStat()[x_colonne]
        
        

        all_modules = pd.concat([agg_data_sur_le_module,all_x_colonne_data],axis=1)

        all_modules.sort_values([x_colonne],ascending=[False],inplace=True)

        all_modules['rang'] = [i for i in  range(1,all_modules[x_colonne].size +1)]

        all_modules = all_modules.drop(columns=[x_colonne])
        # all_modules = pd.concat([temps_sur_le_module,taux_de_reussite_de_tous_les_module],axis=1)
        all_modules_data = all_modules.to_numpy()
        # all_modules
        all_modules_data

        all_modules_data = all_modules_data.T
        x = all_modules_data[1]
        y = all_modules_data[0]
        plt.scatter(x,y)

        plt.title(f'Les points sont des {nom_colonne[0]}')
        plt.xlabel(f"Rang en fonction de : {x_colonne}")
        plt.ylabel(f"{agg_dic_key} ({agg_dic_value})");
        

    def camenbert(self):
        df = self.getStat()
        data_class_A = df.loc[df['taux_de_reussite'] >=  80].size
        data_class_B = df.loc[(df['taux_de_reussite'] >=  60) & (df['taux_de_reussite'] <  80)].size
        data_class_C = df.loc[(df['taux_de_reussite'] >=  50) & (df['taux_de_reussite'] <  60) ].size
        data_class_D = df.loc[(df['taux_de_reussite'] <  50)  ].size

        all_classe_size = df.size

        # data_class_A + data_class_B + data_class_C + data_class_D == all_classe_size

        plt.figure(figsize = (7, 7))
        plt.title("Taux de reussite")
        x = np.array([data_class_A/all_classe_size,data_class_B/all_classe_size,data_class_C/all_classe_size,data_class_D/all_classe_size])
        label = ["A", "B", "C", "D"]

        plt.pie(x, labels=label, autopct = lambda x: str(round(x, 2)) + '%' )
        # plt.legend()

        plt.show()
        
        
    
    
    # les methode privé
    def __normalisation(self,row):
        row.score = 1 if row.score >= 50 else 0
        return row
    
    def __temps_et_score_from_object_id(self,object) :
        df_actor_temps = self.dataset.loc[self.dataset['object_id'] == object].groupby('actor').agg({"temps":['sum'],"score":['max']})

        df_actor_temps = pd.concat([df_actor_temps.temps,df_actor_temps.score],axis=1)
        df_actor_temps.sort_values(['sum'],ascending=[True],inplace=True)

        df_actor_temps = np.array(df_actor_temps.to_numpy().T)

        temps, score_max = df_actor_temps[0],df_actor_temps[1]

        return df_actor_temps[0],df_actor_temps[1]
    
    def __get_rang_score_max_by_module_name(self,nom_module):
        df_actor = self.dataset.loc[self.dataset['object_id'] == nom_module].groupby(['actor']).agg({'score':['max']})
        df_actor = df_actor.score
        df_actor.sort_values(['max'],ascending=[False],inplace=True)

        score_max = df_actor.to_numpy()
        rang = np.array([i for i in range(1, score_max.size+1)])

        return rang,score_max
    
            
            
            
data = DataProcessing(csv_file_name)


# In[13]:


# data.camenbert()


# In[ ]:




