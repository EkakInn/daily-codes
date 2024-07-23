from lib2to3.pgen2.token import N_TOKENS
import dropbox
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()
basedir=os.path.abspath(os.path.dirname(__file__))
logs_folder=f'{basedir}/logs/'

logger.add(f"{logs_folder}dbx_token.log", level="INFO", rotation="100 MB")


def dbx_token():

    # logger.info("Start Dropbox")
    APP_KEY = os.getenv("KEY")
    refresh_token = os.getenv("TOKEN")
    # print(APP_KEY,refresh_token)
    with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
        dbx.users_get_current_account()
        # logger.info("End Dropbox ")
        return dbx

def dropbox_access_token():

    # logger.info("Start Dropbox")
    APP_KEY = os.getenv("KEY")
    refresh_token = os.getenv("TOKEN")
    with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
        dbx.users_get_current_account()
        # logger.info("End Dropbox ")
        return dbx

"""Numan Dropbox TOKEN"""


# def dbx_token():
#     val = os.getenv("N_TOKEN")
#     dbx = dropbox.Dropbox(val)
#     return dbx
#
#
# def dropbox_access_token():
#     val = os.getenv("N_TOKEN")
#     dbx = dropbox.Dropbox(val)
#     return dbx

# TOken
