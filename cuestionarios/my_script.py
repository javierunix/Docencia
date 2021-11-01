import os # para ejecutar comandos externos del S.O. 
import csv #  para trabajar con archivos csv
import random #  para barajar aleatoriamente las respuestas
import pandas as pd
import sys # para poder pasar el fichero de entrada como argumento



filepath = str(sys.argv[1])
filename = os.path.basename(filepath)

header = input("¿Encabezamiento de texto del examen? ")

os.system('mkdir output')

filename_split= filename.split('.')
output_test_md = 'output/' + filename_split[0] + '_test.md'
output_check_md = 'output/' + filename_split[0] + '_check.md'
output_test_pdf = 'output/' + filename_split[0] + '_test.pdf'
output_check_pdf = 'output/' + filename_split[0] + '_check.pdf'




df = pd.read_csv(filename,sep = ";") # se carga en una tabla de pandas el fichero original con las preguntas
df_mode = df.sample(frac = 1).reset_index(drop = True) # se barajan las preguntas para que no aparezcan siempre en el mismo orden
df_mode.to_csv('new_file.csv', sep = ";", index = False)


# abre el archivo entrada en modo de lectura y los de salida en modo de escritura
# hay dos archivos de salida: uno con las preguntas del examen y otro con la clave para corregir las respuestas
with open('new_file.csv', mode='r') as in_file, \
    open(output_check_md, mode='w') as correct_file, \
    open(output_test_md, mode='w') as out_file: 


    csv_reader = csv.reader(in_file, delimiter=';') # lee línea por línea y divide la línea usa como espaciador ";""
    line_count = 0 # inicializa contardor de líneas
    header = "# " + header + "\n"
    out_file.write(header)


    for row in csv_reader:

        if line_count == 0: # omite línea 0
            line_count += 1 # aumenta el contador de línea

        else:
            out_file.write(f'### Pregunta {line_count}\n{row[0]}\n\n') # escribe la pregunta
            key_list = ['A', 'B', 'C', 'D'] # identificadores alfabéticos de las respuestas
            key_count = 0 # contador de los identificadores alfabéticos
            my_list = list(range(1, len(row))) # crea una lista con los índices de cada respuesta
            random.shuffle(my_list) # baraja de modo aleatorio los índices

            for i in my_list: # itera sobre los indices de la respuesta
                out_file.write(f'- [ ] {key_list[key_count]}. {row[i]}\n\n') # escribe la respuesta
                if i == 1:
                    correct_file.write(f'## {line_count}. {key_list[key_count]}\n') # la respuesta correcta siempre era la de la columna 1 del archivo csv
                key_count += 1 # incrementa el contador para el identificador alfabético 


            out_file.write(f'\n') # incluye línea adicional

            line_count += 1

shell_script = 'rm new_file.csv && pandoc '+ output_check_md + ' -s -o ' + output_check_pdf +' && pandoc ' + output_test_md + ' -s -o '+ output_test_pdf
os.system(shell_script)
    