'''
1- conecta
2- para a aplicacao
3- exclui a aplicacao
4- instala aplicaçao --> deploy()
				   		| remote=true -- faz com que o admin utilize o caminho relativo a sua propria instalacao
				   		| targets='NOME_DO_CLUSTER1,NOME_DO_CLUSTER2'
				   		| path='O:/apps/hello.war'  {caminho com forward slashes}
				   		| block=[true/false] faz com que somente o termino do comando dispare o proximo

5- inicializa aplicacao se necessario

********************************************************************************
						ESTADOS DO SERVIDOR
			['RUNNING', 'ADMIN', 'SHUTDOWN', 'FAILED']


						ESTADOS DA APLICACAO
			['NEW', 'ACTIVE', 'PREPARED', 'ADMIN','FAILED']
********************************************************************************
'''
import os
import re
import sys
import time
import java.lang
from java.io import FileInputStream

#CARREGA O ARQUIVO COM PARAMETROS
propInputStream = FileInputStream('O:/temp/PlanoDeMudanca/templateHotDeploy/FileProperties/canest_imediato.properties')
configProps = Properties()
configProps.load(propInputStream)


#remove os espacos em branco dos parametros escritos no arquivo.
#url=configProps.get('param.url'))
#aplicacaoVelha=re.sub(' ','',configProps.get('param.aplicacaoVelha'))
#aplicacaoNova=re.sub(' ','',configProps.get('param.aplicacaoNova'))
#TargetToDeploy=re.sub(' ','',configProps.get('param.TargetToDeploy'))
#caminhoPacoteWar=re.sub(' ','',configProps.get('param.caminhoPacoteWar'))
#numeroPM=re.sub(' ','',configProps.get('param.numeroPM'))

url=configProps.get('param.url')
aplicacaoVelha=configProps.get('param.aplicacaoVelha')
aplicacaoNova=configProps.get('param.aplicacaoNova')
TargetToDeploy=configProps.get('param.TargetToDeploy')
caminhoPacoteWar=configProps.get('param.caminhoPacoteWar')
numeroPM=configProps.get('param.numeroPM')



print url
print aplicacaoVelha
print aplicacaoNova
print TargetToDeploy
print caminhoPacoteWar
print numeroPM
java.lang.Thread.sleep(2000)
print(' --- ')

def registraLog(arrayMsg, mensagem):
	arrayMsg.append(time.strftime("%d/%m/%Y - %H:%M:%S") + ' | ' + mensagem +'\n')

def salvaLog(arquivo, arrayMsg):
	arquivo.writelines(arrayMsg)
	arquivo.close()

#determina o instante inicial para medir tempo de execucao
tmr_horarioInicioSrcpt = time.time()

arq = open('O:/temp/PlanoDeMudanca/templateHotDeploy/logs/'+ aplicacaoVelha +'_['+numeroPM+'].log', 'a')
texto = []
registraLog(texto, ' -> Inicializando execução do script.')

redirect('O:/temp/PlanoDeMudanca/templateHotDeploy/logs/'+ aplicacaoVelha +'_['+numeroPM+'].wlst', 'false')
print('CONECTANDO AO DOMINIO')
try:
	connect('cristiano', 'SENHA', url)
	#connect(userConfigFile='O:/temp/PlanoDeMudanca/templateHotDeploy/ChaveCristiano/TJRS_PROD/cristianoConfig.security', userKeyFile='O:/temp/PlanoDeMudanca/templateHotDeploy/ChaveCristiano/TJRS_PROD/cristianoKey.security',url='wls.prod.tjrs.gov.br:7301')
	print(':::::::--- (1) CONECTOU ---:::::::')
	print('\n\n --- \n\n')
except:
	print('\n\n --- \n\n')
	print('NÂO FOI POSSIVEL CONECTAR AO DOMINIO')
	print('\n\n --- \n\n')
	exit()

import os
import re
import sys
import time
import java.lang

registraLog(texto, ' -> Conectou ao ADMIN.')
java.lang.Thread.sleep(1000)
appToUnDeploy=''
cd('serverConfig:/AppDeployments')
aplicacoesEncontradas = cmo.getAppDeployments()
for aplicacaoInstalada in aplicacoesEncontradas:
	if aplicacaoInstalada.getName().find(aplicacaoVelha) !=-1:
		appToUnDeploy = aplicacaoInstalada.getName()

print appToUnDeploy
java.lang.Thread.sleep(1000)
print ' -> Parando a aplicacao '
java.lang.Thread.sleep(500)

''' INDISPONIBILIZA APP '''
progress=stopApplication(appName=appToUnDeploy, force='true', block='false', retireTimeout=0)
print('\n\n --- \n\n')
print(':::::::--- (2) PARANDO A APLICACAO ---:::::::')
print('\n\n --- \n\n')

registraLog(texto, ' -> Parando a aplicacao ' + appToUnDeploy +' para Undeploy().')

''' VERIFICA A SITUACAO DA APP ATE ESTAR OFF'''
progress.printStatus()
while true:
	if (progress.isRunning() != 0):
		execfile('./inc/imprimeDelay.py')
		print '...............................................................'
		print 'Application: ', appToUnDeploy, 'nao parou ainda...............'
		print '...............................................................'
	else:
		print '--------------------------------------------------------------'
		print '--------------------------------------------------------------'
		print 'Application: ', appToUnDeploy, ' PAROU!! --------------------'
		print '--------------------------------------------------------------'
		print '--------------------------------------------------------------'
		break

registraLog(texto, ' -> Aplicacao: '+ appToUnDeploy +' parada.')
tmr_inicioOffLine =  time.time()

'''ARRANCA A APP DO AMBIENTE'''
print('\n\n --- \n\n')
print(':::::::--- (3) ARRANCANDO A APLICACAO ---:::::::')
print('\n\n --- \n\n')
java.lang.Thread.sleep(2000)

try:
	registraLog(texto, ' -> Undeploy('+appToUnDeploy+').')
	progress=undeploy(appName=appToUnDeploy, force='true', block='false')
except Exception, err:
    print Exception, err

''' VERIFICA A SITUACAO DA APP ATE ESTAR OFF'''
progress.printStatus()
while true:
	if (progress.isRunning() != 0):
		execfile('./inc/imprimeDelay.py')
		print '............................................................'
		print 'Application: ', appToUnDeploy, ' nao excluiu ainda.........'
		print '............................................................'
	else:
		print '------------------------------------------------------------'
		print '------------------------------------------------------------'
		print 'Application: ', appToUnDeploy, ' FORA DO AMBIENTE!!--------'
		print '------------------------------------------------------------'
		execfile('./inc/imprimeOK.py')
		break

registraLog(texto, ' -> Aplicacao: '+ appToUnDeploy +' fora do ambiente.')
print('\n\n --- \n\n')
print '.:.:.:.:.:.:.:.:.:.:.:.:.: Iniciando deploy .:.:.:.:.:.:.:.:.:.:.:.:'
java.lang.Thread.sleep(1500)
print('\n\n --- \n\n')

registraLog(texto, ' -> Deploy('+ aplicacaoNova +')')

progress=deploy(appName=aplicacaoNova, path=caminhoPacoteWar,targets=TargetToDeploy, remote='true', block='false')

print('\n\n --- \n\n')
''' VERIFICA A SITUACAO DA APP ATE ESTAR INSTALADA'''
print('\n\n --- \n\n')
progress.printStatus()
while true:
	if (progress.isRunning() != 0):
		execfile('./inc/imprimeDelay.py')
		print '.............................................................'
		print 'Application: ', aplicacaoNova, ' NAO INSTALOU AINDA..........'
		java.lang.Thread.sleep(1000)
		print '.............................................................'
	else:
		print '------------------------------------------------------------'
		print '------------------------------------------------------------'
		print 'Application: ', aplicacaoNova, ' INSTALOU.....'
		print '------------------------------------------------------------'
		print '------------------------------------------------------------'
		execfile('./inc/imprimeOK.py')
		break

cd('serverConfig:/AppDeployments')
aplicacoesInstaladas = cmo.getAppDeployments()
for aplicacao in aplicacoesInstaladas:
	if aplicacao.getName().find(aplicacaoNova) !=-1:
		aplicacaoInstalada = aplicacao.getName()

print aplicacaoInstalada
java.lang.Thread.sleep(1000)
registraLog(texto, ' -> Inicializando '+ aplicacaoInstalada +'.')
try:
	progress=startApplication(appName=aplicacaoInstalada, block='false')
	print('\n\n --- \n\n')
	''' VERIFICA A SITUACAO DA APP ATE ESTAR INSTALADA'''
	print('\n\n --- \n\n')
except:
	print('\n\n --- \n\n')
	print(':::::::--- (3) APLICACAO INICIALIZADA ---:::::::')
	print('\n\n --- \n\n')

progress.printStatus()
while true:
	if (progress.isRunning() != 0):
		execfile('./inc/imprimeDelay.py')
		print '................................................'
		print 'Application: ', aplicacaoInstalada, ' OFFLINE AINDA...'
		print '................................................'
		java.lang.Thread.sleep(500)
	else:
		registraLog(texto, ' -> Aplicação ONLINE.')
		tempoTotalExecucao = "Tempo de execucão do script: %s seconds.		" % round(time.time() - tmr_horarioInicioSrcpt, 2)
		tempoTotalOffLine = "Tempo de downtime da app: %s seconds.	" % round(time.time() - tmr_inicioOffLine, 2)
		registraLog(texto, ' -> Fim da execucão.')
		execfile('./inc/imprimeOK.py')
		break

texto.append('\n')
texto.append('\n')
texto.append('------------------------------------------------------------------------------------\n')
texto.append(tempoTotalExecucao+'\n')
texto.append(tempoTotalOffLine+'\n')

salvaLog(arq, texto)
java.lang.Thread.sleep(5000)
print('\n\n --- \n\n')
print 'bye bye'
print('\n\n --- \n\n')
disconnect()