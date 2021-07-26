# -*- coding: utf-8 -*-
"""
Logger para aplicaciones Django.

settings.py en Django:

#---------


#---------



    import tlalogger
    logger = tlalogger.dj_mylogger(__file__)

    logger.critical("Hola")
    logger.error("Hola")
    logger.warning("Hola")
    logger.info("Hola")
    logger.debug("Hola")


"""
import inspect
#import pprint
import logging
#import datetime
#import os

from django.conf import settings

def dj_mylogger(a__file__a):
    """
    Devolvemos un logger que va asociado al nombre de la aplicacion Django
    que se está ejecutando. Esto es necesario porque los loggers en Django 
    deben estar previamente definidos en settings.py no se pueden nombrar "al vuelo".
    Previamente hemos definido en settings.py un logger por aplicacion.
    
    Desde dónde queramos llamar al logger:
        import tlalogger
        logger = tlalogger.dj_mylogger(__file__)
        logger.debug("Valor de l_ejemplo (%s) ",repr(l_ejemplo))
    """
    dj_app = a__file__a.replace(settings.BASE_DIR,'').split('/')[1]
    logger = logging.getLogger(dj_app)
    return logger


# def nuevo_fichero_log(filename=None):
#     """
#     """
#     if filename == None:
#         ahora=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#         #filename=config.dir_tmp+'/'+'serialcom_sniff_'+ahora[0:19]+'.log'
#         filename='/tmp/tb800/app/'+'tb800app_'+ahora[0:15]+'.log'
#     try:
#         os.mkdir('/tmp/')
#     except: 
#         pass
#     try:
#         os.mkdir('/tmp/tb800/')
#     except: 
#         pass
#     try:
#         os.mkdir('/tmp/tb800/app/')
#     except: 
#         pass
#     
#     logger=logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     lh = logging.StreamHandler(open(filename,'w'))
#     lh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s(): %(message)s',))
#     logger.addHandler(lh)
#     logger.removeHandler(logger.handlers[0])
# 
# 
# 
def donde_estoy():
    """Returns an informative prefix for verbose debug output messages"""
    import pprint
    s = inspect.stack()
    module_name = inspect.getmodulename(s[1][1])
    func_name = s[1][3]
#     pprint.pprint(s[1])
#     print os.path.dirname(__file__).split('/')[-1]
    if func_name=='<module>':
        func_name='__main__'

    return '%s.%s' % (module_name, func_name)
    



# def mylogger(str_donde_estoy):
#     """
#     """
#     logger = logging.getLogger(str_donde_estoy)
#     
#     return logger


## No valido para Django::
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(name)s(): %(message)s',
#                     #filename=filename,
#                     #filemode='w',
#                     )
# nuevo_fichero_log()

#logging.info('Iniciando Logging ...')
#logging.info('Guardando log en %s', filename)
#logger = logging.getLogger(inspect.getframeinfo(inspect.currentframe()).function)
