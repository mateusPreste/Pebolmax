import configparser

config = configparser.ConfigParser()
configObject = config.read('settings.conf')

myplayer = config['player']['mainPlayer']

print(myplayer)