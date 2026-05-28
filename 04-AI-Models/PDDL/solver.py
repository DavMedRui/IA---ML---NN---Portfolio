
import sys
import requests

data = {'domain': open(sys.argv[1], 'r', encoding='utf-8').read(),
        'problem': open(sys.argv[2], 'r', encoding='utf-8').read()}

PLANNER_URL = 'https://solver.planning.domains:5001'

sendPlanning = requests.post(PLANNER_URL+'/package/dual-bfws-ffparser/solve', verify=False, json=data, timeout=5000)
sendPlanning = sendPlanning.json()

data = {
    'adaptor': "planning_editor_adaptor"
}

GetPlanningResult = requests.post(PLANNER_URL+sendPlanning['result'], verify=False, json=data, timeout=5000)
GetPlanningResult = GetPlanningResult.json()

print(GetPlanningResult['plans'][0]['result']['plan']) #Mostramos el plan por consola

#Comprobamos que exista el plan
if GetPlanningResult['plans'][0]['result']['plan']:
    # Procesar el plan si está presente en la respuesta
    with open(sys.argv[3], 'w', encoding='utf8') as f:
        f.write('\n'.join([act['name'] for act in GetPlanningResult['plans'][0]['result']['plan']]))
