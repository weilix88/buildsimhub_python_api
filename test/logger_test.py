from BuildSimHubAPI.logger import BuildSimLogger

logger = BuildSimLogger()
logger.write_in_message('a', 'b', 'c', 'd', 'e')
logger.write_in_csv()
