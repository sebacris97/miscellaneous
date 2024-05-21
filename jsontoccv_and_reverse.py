import sys
import PySimpleGUI as sg
import csv
import json


def jsonToCsv(dic,cabecera,destino):

  if destino=='':
    destino='example.csv'
  elif destino[-4:]!='.csv':
    destino=destino+'.csv'
    
  try:
    f = open(destino, 'w')
  except:
    sg.Popup("No se pudo completar la operacion")
    return
  aux={}
  with f:
    writer = csv.DictWriter(f, fieldnames=cabecera)    
    writer.writeheader()
    for i in dic.keys():
      for k in cabecera:
          aux[k]=str(dic[i][k])
      writer.writerow(aux)

  f.close()

    
def csvToJson(origen,destino):
    try:
        archivoOrigen=open(origen, 'r', encoding = 'ISO-8859-1')
    except:
        salir()
        
    with archivoOrigen as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        csvfile.close()

    if destino=='':
        destino='example.json'
    elif destino[-5:]!='.json':
        destino=destino+'.json'
        
    try:
        archivoDestino=open(destino, 'w', encoding = "ISO-8859-1")
    except:
        salir()
        
    with archivoDestino as jsonfile:
        json.dump(rows,jsonfile)




def crearTabla(data,cabecera):

    layout = [[sg.Table(values=data[:],
                        headings=cabecera,
                        max_col_width=25,
                        auto_size_columns=True, justification='center',
                        alternating_row_color='lightblue',
                        num_rows=min(len(data), 24))],
              [sg.Text("Destino"),sg.Input(size=(35,1),key='destino'),sg.SaveAs("Browse")],
              [sg.Text("Formato"),sg.Button('JSON',pad=(10,1)),sg.Text(' '*10),sg.Button('CSV')],
              [sg.Text("lineas leidas: "+str(len(data)) )]
           ]
    return layout



    

def salir(s="Error leyendo el archivo"):
    sg.Popup(s)
    sys.exit()


#esta fucion parsea el .json formato 2 al formato 1
def parseo(dic):
      aux = {}
      cont = 0
      for i in range(len(dic)):
          aux[str(cont)]=dic[i]
          cont += 1
      return aux
    

    
#esta funcion valida si .json es del formato 3
def otroFormato(dic):
    a=list(dic.keys())
    if len(a)==1:
        return isinstance(dic[a[0]],list)
    

def workWithCSV(archivo,data,cabecera):
    with archivo as file:
        reader = csv.reader(file)
        cabecera = next(reader)
        try:
            data = list(reader)
        except:
            salir()
            
    return data,cabecera



#
#Este programa pretende soportar 3 formas validas de .json
#comprobadas en jsonlint.com (pagina proporcionada por un
#ayudante en el foro de catedras)
#
#Puede ser que el json venga de tres formas:
    #1: {'1':{dato1:valor1},'2':{dato2:valor2},'3':{dato3:valor3}}
    #2: [{dato1:valor1},{dato2:valor2},{dato3:valor3}]
    #3: {'datos':[{dato1:valor1},{dato2:valor2},{dato3:valor3}]}
#las 3 formas son formatos validos de .json, y este programa espera recibir
#el .json en alguno de estos 3 formatos
#
def workWithJSON(archivo,data,cabecera):

    dic = json.load(archivo) #por defecto usamos el formato 1

    if isinstance(dic,list): #me fijo si viene en el formato 2
        dic=parseo(dic)      #si no viene lo convierto a formato 1

    elif otroFormato(dic):    #me fijo si viene en formato 3
        a=list(dic.keys())[0] 
        dic=parseo(dic[a])
      #si no viene lo convierto a formato 1
      #tomando directamente la lista del diccionario
      #(y procedo de manera similar que si fuese formato 2)

    cabecera = list(dic['0'].keys()) #todas las cabeceras son iguales
                             #asi que agarro el del primer elemento

    for i in dic.keys():

        aux=[]
        for k in cabecera:
            aux.append(str(dic[i][k]))
        data.append(aux)

    return data, cabecera, dic
    

def main():

    sg.Popup("Seleccione el archivo .csv o .json a mostrar")
    filename = sg.PopupGetFile('filename to open',no_window=True, file_types=(("CSV Files","*.csv"),("JSON Files","*.json")))

    if filename == '':
        sys.exit()
 
    data = []     #datos de la tabla
    cabecera = [] #cabecera de la tabla

    
    if filename is not None:
        
        try:
            archivo=open(filename, 'r')
        except:
            salir()

        if filename[-4:]=='.csv': #me fijo si es .csv
            data,cabecera = workWithCSV(archivo,data,cabecera)

        elif filename[-5:]=='.json': #me fijo si es .json
            data,cabecera,dic = workWithJSON(archivo,data,cabecera)
                    

    sg.SetOptions(element_padding=(0, 0))
    window = sg.Window('TABLA').Layout(crearTabla(data,cabecera))

    while True:
        event, values = window.Read()
        
        if event==None:
            sys.exit()
            
        if event=='CSV':
            if filename[-4:]=='.csv':
                sg.Popup("El archivo Ya esta en ese formato")
            else:
                jsonToCsv(dic,cabecera,values['destino'])
                sg.Popup("conversion exitosa")
                
        elif event=='JSON':
            if filename[-5:]=='.json':
                sg.Popup("El archivo ya esta en ese formato")
            else:
                csvToJson(filename,values['destino'])
                sg.Popup("conversion exitosa")


    sys.exit()

if __name__=="__main__":
    main()
