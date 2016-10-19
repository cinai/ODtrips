import json
import csv
import os
import pickle 
import pandas as pd
from os import listdir
from os.path import isfile, join
from ODmaps.processingtools import tfe
from ODmaps.processingtools import auxiliar_functions
from django.conf import settings

#TODO: Falta agregar los datos
def get_rois(usuario):
	#importar datos relativos al usuario
	datos_abril = pd.read_csv(os.path.join(settings.BASE_DIR,'ODmaps','data','etapas_2013_abril_allyearsids_10_100000.csv'))
	datos_usuario_abril = datos_abril[datos_abril['id']==usuario].copy()
	datos_usuario_abril = auxiliar_functions.frame_config(datos_usuario_abril)
	datos_septiembre = pd.read_csv(os.path.join(settings.BASE_DIR,'ODmaps','data','etapas_2013_septiembre_allyearsids_10_100000.csv'))
	datos_usuario_septiembre = datos_septiembre[datos_septiembre['id']==usuario].copy()
	datos_usuario_septiembre = auxiliar_functions.frame_config(datos_usuario_septiembre)
	del datos_abril
	del datos_septiembre
	#extraer rois #todo: change parameter
	abril_rois = tfe.get_ROIs(datos_usuario_abril,0.7,500)
	septiembre_rois = tfe.get_ROIs(datos_usuario_septiembre,0.7,500)
	print("Aqui vienen el porcentaje de rois")
	print(abril_rois[1])
	print(septiembre_rois[1])

	return [abril_rois[0],septiembre_rois[0]]
