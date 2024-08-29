import shutil

shutil.rmtree('Simulation/Resource/scenariorun-data')
shutil.copytree('code/run_templates/sample/scenariorun-data', 'Simulation/Resource/scenariorun-data')