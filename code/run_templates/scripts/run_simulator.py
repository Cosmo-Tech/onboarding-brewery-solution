import os

import csm.engine as CosmoEngine

from get_logger import logger

simulator = CosmoEngine.LoadSimulator("BusinessApp_Simulation")
logger.info("Simulator loaded")

if ((amqp_consumer_adress := os.environ.get("CSM_PROBES_MEASURES_TOPIC")) is not None
        and "CSM_CONTROL_PLANE_TOPIC" in os.environ):
    # Remove local CSV consumers
    for consumer in simulator.GetConsumers():
        simulator.DestroyConsumer(consumer)
    # Instantiate AMQP consumers to send data to the cloud service
    simulator.InstantiateAMQPConsumers("Simulation", amqp_consumer_adress)
    logger.info("AMQP Consumer instantiated")

logger.info("Starting simulation")
simulator.Run()
logger.info("Simulation finished")
