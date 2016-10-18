from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, render
from django.utils import timezone
from django.conf import settings
import json
import csv
import os
import pickle 
from os import listdir
from os.path import isfile, join
from ODmaps.processingtools import queri

def index(request):
	return render(request,'test2.html',)

def test2(request):
	return render_to_response('test2.html',)

def visualizador(request):
	sequence_name = 'sequence'
	usuario = "?"
	corte_temporal = "?"
	if request.method == 'GET':
		sequence_name = request.GET.get('id','sequence')
		folder_name = request.GET.get('folder','')
	# asumo que viene en el formato idusuario_indexusuario_mes
	if(sequence_name!='sequence'):
		sequence_data = sequence_name.split('_')
		usuario = sequence_data[0]
		corte_temporal = sequence_data[1]
	subida = []
	bajada = []
	tiempo = []
	netapa = []
	nviaje = []
	tipo_dia = []
	counter = 0
	sequence = []
	dict_paradas = {}
	file_name =  sequence_name + '.csv'
	file_path = os.path.join(settings.BASE_DIR,'static','datos',file_name)
	if(folder_name != ''):
		file_path = os.path.join(settings.BASE_DIR,'static','datos',folder_name,file_name)

	with open(file_path) as csvfile:	
		reader = csv.DictReader(csvfile)
		for row in reader:
			#aqui hay que pensaarlo un poco mas, por la bajada
			tiempo.append(row['tiempo_subida'])
			tipo_dia.append(row['tipo_dia'])
			nviaje.append(row['nviaje'])
			netapa.append(row['netapa'])
			subida.append(row['par_subida'])
			bajada.append(row['par_bajada'])
			dict_paradas = {'subida':subida[counter],'bajada': bajada[counter]}
			sequence.append(dict_paradas)
			counter += 1
	to_json = {
		"tiempo": tiempo,
		"nviaje": nviaje,
		"netapa": netapa,
		"subida": subida,
		"bajada": bajada,
		"sequence": sequence,
		"tipo_dia": tipo_dia,
		"usuario": usuario,
		"corte_temporal": corte_temporal
	}
	js_data = json.dumps(to_json)
	return render(request,'visualizador.html',{"jsdatos":js_data})

def visualizador_normalizado(request):
	sequence_name = 'sequence'
	usuario = "?"
	corte_temporal = "?"
	if request.method == 'GET':
		sequence_name = request.GET.get('id','sequence')
		folder_name = request.GET.get('folder','')
	# asumo que viene en el formato idusuario_indexusuario_mes
	if(sequence_name!='sequence'):
		sequence_data = sequence_name.split('_')
		usuario = sequence_data[0]
		corte_temporal = sequence_data[1]
	subida = []
	bajada = []
	tiempo = []
	netapa = []
	nviaje = []
	tipo_dia = []
	counter = 0
	sequence = []
	dict_paradas = {}
	file_name =  sequence_name + '.csv'
	file_path = os.path.join(settings.BASE_DIR,'static','datos',file_name)
	if(folder_name != ''):
		file_path = os.path.join(settings.BASE_DIR,'static','datos','sequences_norm2',folder_name,file_name)

	with open(file_path) as csvfile:	
		reader = csv.DictReader(csvfile)
		for row in reader:
			#aqui hay que pensaarlo un poco mas, por la bajada
			tiempo.append(row['tiempo_subida'])
			tipo_dia.append(row['tipo_dia'])
			nviaje.append(row['nviaje'])
			netapa.append(row['netapa'])
			subida.append(row['par_subida'])
			bajada.append(row['par_bajada'])
			dict_paradas = {'subida':subida[counter],'bajada': bajada[counter]}
			sequence.append(dict_paradas)
			counter += 1
	to_json = {
		"tiempo": tiempo,
		"nviaje": nviaje,
		"netapa": netapa,
		"subida": subida,
		"bajada": bajada,
		"sequence": sequence,
		"tipo_dia": tipo_dia,
		"usuario": usuario,
		"corte_temporal": corte_temporal
	}
	js_data = json.dumps(to_json)
	return render(request,'visualizador.html',{"jsdatos":js_data})

def compare(request):
	sequence_name = 'sequence'
	usuario = "?"; corte_temporal = "?"
	ct1 = 'abril';	ct2 = 'septiembre'
	subida = [];bajada = [];tiempo = []
	netapa = [];nviaje = [];tipo_dia = []
	counter = 0;sequence = [];dict_paradas = {}
	subida2 = [];bajada2 = [];tiempo2 = []
	netapa2 = [];nviaje2 = [];tipo_dia2 = []
	counter2 = 0;sequence2 = [];dict_paradas2 = {}	
	if request.method == 'GET':	
		sequence_name = request.GET.get('id','sequence')
		folder_name = request.GET.get('folder','')
	# asumo que viene en el formato idusuario_indexusuario
	if(sequence_name!='sequence'):
		sequence_data = sequence_name.split('_')
		usuario = sequence_data[0]
		#index_usuario = sequence_data[1]
		#corte_temporal = sequence_data[1]
		file_name =  sequence_name + '_' + ct1 + '.csv'
		file_name2 =  sequence_name + '_' + ct2 + '.csv'
		if(folder_name != ''):
			file_path1 = os.path.join(settings.BASE_DIR,'static','datos',folder_name,file_name)
			file_path2 = os.path.join(settings.BASE_DIR,'static','datos',folder_name,file_name2)
		else:
			file_path1 = os.path.join(settings.BASE_DIR,'static','datos',file_name)
			file_path2 = os.path.join(settings.BASE_DIR,'static','datos',file_name2)
		with open(file_path1) as csvfile:	
			reader = csv.DictReader(csvfile)
			for row in reader:
				#aqui hay que pensaarlo un poco mas, por la bajada
				tiempo.append(row['tiempo_subida'])
				tipo_dia.append(row['tipo_dia'])
				nviaje.append(row['nviaje'])
				netapa.append(row['netapa'])
				subida.append(row['par_subida'])
				bajada.append(row['par_bajada'])
				dict_paradas = {'subida':subida[counter],'bajada': bajada[counter]}
				sequence.append(dict_paradas)
				counter += 1
		abril_rois, septiembre_rois = queri.get_rois(int(usuario))

		with open(file_path2) as csvfile:	
			reader = csv.DictReader(csvfile)
			for row in reader:
				#aqui hay que pensaarlo un poco mas, por la bajada
				tiempo2.append(row['tiempo_subida'])
				tipo_dia2.append(row['tipo_dia'])
				nviaje2.append(row['nviaje'])
				netapa2.append(row['netapa'])
				subida2.append(row['par_subida'])
				bajada2.append(row['par_bajada'])
				dict_paradas2 = {'subida':subida2[counter2],'bajada': bajada2[counter2]}
				sequence2.append(dict_paradas2)
				counter2 += 1
	to_json = {
		"tiempo": tiempo,
		"nviaje": nviaje,
		"netapa": netapa,
		"subida": subida,
		"bajada": bajada,
		"sequence": sequence,
		"tipo_dia": tipo_dia,
		"usuario": usuario,
		"corte_temporal": ct1,
		"tiempo2": tiempo2,
		"nviaje2": nviaje2,
		"netapa2": netapa2,
		"subida2": subida2,
		"bajada2": bajada2,
		"sequence2": sequence2,
		"tipo_dia2": tipo_dia2,
		"corte_temporal2": ct2,
		"abril_rois": abril_rois,
		"septiembre_rois":septiembre_rois
	}
	js_data = json.dumps(to_json)
	return render(request,'compare.html',{"jsdatos":js_data})

def all_trips(request):
	sequence_name = 'sequence'
	usuario = "?"
	ct1 = "abril"
	ct2 = "septiembre"
	if request.method == 'GET':
		folder_name = request.GET.get('folder','')
	subida = [];bajada = [];tiempo = []
	netapa = [];nviaje = [];tipo_dia = []
	counter = 0;sequence = [];dict_paradas = {}
	subida2 = [];bajada2 = [];tiempo2 = []
	netapa2 = [];nviaje2 = [];tipo_dia2 = []
	counter2 = 0;sequence2 = [];dict_paradas2 = {}

	file_name =  sequence_name + '.csv'
	file_path = ''
	folder_path = os.path.join(settings.BASE_DIR,'static','datos','cambioDeComport')
	if(folder_name != ''):
		folder_path = os.path.join(settings.BASE_DIR,'static','datos',folder_name)

	ct1_files = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f)) and ct1 in f]
	ct2_files = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f)) and ct2 in f]

	for f in ct1_files:
		with open(f) as csvfile:	
			reader = csv.DictReader(csvfile)
			for row in reader:
				#aqui hay que pensaarlo un poco mas, por la bajada
				tiempo.append(row['tiempo_subida'])
				tipo_dia.append(row['tipo_dia'])
				nviaje.append(row['nviaje'])
				netapa.append(row['netapa'])
				subida.append(row['par_subida'])
				bajada.append(row['par_bajada'])
				dict_paradas = {'subida':subida[counter],'bajada': bajada[counter]}
				sequence.append(dict_paradas)
				counter += 1
	for f in ct2_files:
		with open(f) as csvfile:	
			reader = csv.DictReader(csvfile)
			for row in reader:
				#aqui hay que pensaarlo un poco mas, por la bajada
				tiempo2.append(row['tiempo_subida'])
				tipo_dia2.append(row['tipo_dia'])
				nviaje2.append(row['nviaje'])
				netapa2.append(row['netapa'])
				subida2.append(row['par_subida'])
				bajada2.append(row['par_bajada'])
				dict_paradas2 = {'subida':subida2[counter2],'bajada': bajada2[counter2]}
				sequence2.append(dict_paradas2)
				counter2 += 1
	to_json = {
		"tiempo": tiempo,
		"nviaje": nviaje,
		"netapa": netapa,
		"subida": subida,
		"bajada": bajada,
		"sequence": sequence,
		"tipo_dia": tipo_dia,
		"usuario": usuario,
		"corte_temporal": ct1,
		"tiempo2": tiempo2,
		"nviaje2": nviaje2,
		"netapa2": netapa2,
		"subida2": subida2,
		"bajada2": bajada2,
		"sequence2": sequence2,
		"tipo_dia2": tipo_dia2,
		"corte_temporal2": ct2,
		"abril_rois": [],
		"septiembre_rois":[]
	}
	js_data = json.dumps(to_json)
	return render(request,'plot_transactions.html',{"jsdatos":js_data})