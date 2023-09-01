from loguru import logger

logger.add("logs.log", level='INFO', colorize=False)

logger.info(f'START LOGGER')
