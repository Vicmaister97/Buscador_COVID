#!/bin/bash
FILE_DEBUG=/home/auto-vk/Escritorio/auto-programs/Buscador_COVID/DEBUG/debug.txt
FECHA_HOY=$(date +%d_%m_%Y)
echo -e "\n\n" >> $FILE_DEBUG
date >> $FILE_DEBUG

### COMPROBAMOS QUE ES LUNES, MIERCOLES O VIERNES!!! Dia de toma de datos
if [ $(date +%u) -ne 1 ] && [ $(date +%u) -ne 3 ] && [ $(date +%u) -ne 5 ]; then
    echo 'Lo siento, no es día de toma de datos. FIN' >> $FILE_DEBUG
    exit
fi
if [ $(date +%u) -eq 1 ] || [ $(date +%u) -eq 2 ]; then		## lunes o miercoles
	NEXT_DATE="$(date --date='+2 day' +%Y-%m-%d)"
fi
if [ $(date +%u) -eq 5 ]; then								## viernes
	NEXT_DATE="$(date --date='+3 day' +%Y-%m-%d)"
fi

# Ponemos el formato de rtcwake: Y-m-d
echo "DIA SIGUIENTE DE TOMA DE DATOS:" >> $FILE_DEBUG
echo $NEXT_DATE >> $FILE_DEBUG

## COMPROBAMOS QUE NO SE HAN ENVIADO YA LOS DATOS (HOY)
FILE="/home/auto-vk/Escritorio/auto-programs/Buscador_COVID/check_auto/"
FILE=$FILE$FECHA_HOY
#echo $FILE
if test -f "$FILE"; then
	echo 'Ya se han enviado HOY los datos, FIN' >> $FILE_DEBUG
	exit
fi

## EJECUTAMOS EL BUSCADOR
echo "STARTUP-SCRIPT que ejecuta el Buscador-COVID3.py" >> $FILE_DEBUG
cd /home/auto-vk/Escritorio/auto-programs/Buscador_COVID
sleep 30	# Esperamos 30 segundos para que las conexiones se puedan realizar
python3 Buscador-COVID3.py
echo "FINALIZADO EL BUSCADOR!!!" >> $FILE_DEBUG
echo "Enviamos los datos (POR HACER)" >> $FILE_DEBUG

## CREAMOS EL FICHERO PARA DECIR QUE HOY SE TOMARON(ENVIARON next step) YA LOS DATOS
touch $FILE
echo "Creado fichero con fecha actual en check_auto"

## PROGRAMAMOS SIGUIENTE ENCENDIDO!!!
NEXT_DATE="$NEXT_DATE"
HOUR=" 12:00:00"
PROG=$NEXT_DATE$HOUR
DESIRED=$((`date +%s -d "$PROG"`))

rtcwake -m no -t $DESIRED >> $FILE_DEBUG
## APAGAR??