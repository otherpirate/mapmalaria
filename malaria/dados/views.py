#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from malaria.dados.models import CIDADE, PACIENTE
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_text
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.sites.models import get_current_site
from django.contrib.staticfiles import finders
import os

def index(request):    
    vTemplate = get_template('index.html')
    vSaida = vTemplate.render(Context({'vSite': ('http://' + get_current_site(request).domain)}))
    return HttpResponse(vSaida)

def mapa(request):
    vArquivo = open(os.path.dirname(os.path.dirname(__file__)) + '/staticfiles/js/pontos.json', 'w')
    vArquivo.write('[\n')

    vCidades   = CIDADE.objects.all()
    vPacientes = PACIENTE.objects.all() 

    vSaida = ''

    vPrimeiro = True; 
    for vCidade in vCidades:        
        vPassa = True
        if (request.method == "POST"):
            vPassa = False
            if ((request.POST.get("edCidade") != "") and
                (request.POST.get("cbUF") != "")):
                vPassa = (vCidade.CID_NOME.upper().find(request.POST.get("edCidade").upper()) >= 0)
                if (vPassa):
                    vPassa = (vCidade.CID_UF.upper().find(request.POST.get("cbUF").upper()) >= 0)
            elif (request.POST.get("edCidade") != ""):
                vPassa = (vCidade.CID_NOME.upper().find(request.POST.get("edCidade").upper()) >= 0)
            elif (request.POST.get("cbUF") != ""):
                vPassa = (vCidade.CID_UF.upper().find(request.POST.get("cbUF").upper()) >= 0)

        if (vPassa):
            vTotal = 0;

            #for vPaciente in vPacientes:
                #vCidadePac = vPaciente.CID_CODIGO_NOT;
                #if (vCidadePac == vCidade.CID_CODIGO):
                    #vTotal = vTotal + 1
                
            if (vPrimeiro == False):
                vArquivo.write(',')
                vArquivo.write('\n')

            vPrimeiro = False;
            vArquivo.write('{"Id": ')
            vArquivo.write(str(vCidade.CID_CODIGO))
            vArquivo.write(',"Latitude": ')
            vArquivo.write(str(vCidade.CID_LATITUDE))
            vArquivo.write(',"Longitude": ')
            vArquivo.write(str(vCidade.CID_LONGITUDE))
            vArquivo.write(',"Descricao": "')
            vArquivo.write(smart_str(vCidade.CID_NOME))
            vArquivo.write('/' + str(vCidade.CID_UF))
            vArquivo.write(smart_str('<br>Total de Notificacoes: '))
            vArquivo.write(str(vTotal) + '"')
            vArquivo.write('}')        
        
    vArquivo.write(']')
    vArquivo.close();

    vContext = {'vSaida': vSaida, 'vSite': ('http://' + get_current_site(request).domain)}
    vContext.update(csrf(request))
    return render_to_response("mapa.html", vContext)    

def informativo(request):    
    vTemplate = get_template('informativo.html')
    vSaida = vTemplate.render(Context({'vSite': ('http://' + get_current_site(request).domain)}))
    return HttpResponse(vSaida)

def estatisticas(request):    
    vTemplate = get_template('estatisticas.html')
    vSaida = vTemplate.render(Context({'vSite': ('http://' + get_current_site(request).domain)}))
    return HttpResponse(vSaida)

def sobre(request):    
    vTemplate = get_template('sobre.html')
    vSaida = vTemplate.render(Context({'vSite': ('http://' + get_current_site(request).domain)}))
    return HttpResponse(vSaida)