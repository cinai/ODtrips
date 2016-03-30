from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, render
from django.utils import timezone
from django.conf import settings
import json
import csv
import os

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
		usuario = sequence_data[1]
		corte_temporal = sequence_data[2]
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