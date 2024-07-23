"""
Step 0 : Get the New Video List from DB
Step 1 : Download Video from Dropbox URL (get from DB)
Step 2 : Applied Algorithm 
Step 3 : Save Incident Values into DB

"""

import os
from loguru import logger #Logger Modules Import
from subprocess import run as subprocess_run #Calling Only Required Function
# from sys import platform 
import sys

# Local Modules
from database_connection import ArgusDB
from analysis_with_area import draw_boundary_box

# Logging File Creation
SERVER_ID=2


camera_id='cam3'
customer_id='1005' #Ganecos

# Path Define
basedir=os.path.abspath(os.path.dirname(__file__))
logs_folder=f'{basedir}/logs/'
device_video_path=f'{basedir}/{camera_id}_videos/'
device_video_json = f'{basedir}/{camera_id}_videos_json/un_uploaded_json/'
device_video_json_uploaded=f'{basedir}/{camera_id}_videos_json/uploaded_json/'
device_frames=f'{basedir}/{camera_id}_frames/'


#######################  logger Define   ######################
logger.add(f'{logs_folder}download_video.log',level="INFO",rotation='50 MB')


def folder_creation(folder_name):
    try:
        logger.info('_Folder Creation Started')
        os.makedirs(folder_name,exist_ok=True)
        logger.info(f"_Folder Created {folder_name}")
    except Exception as Err:
        logger.warning(f'Issue in Folder Creation {Err}')


folder_creation(device_video_path)
folder_creation(device_video_json)
folder_creation(device_video_json_uploaded)
folder_creation(device_frames)



def download_video(url, output_file_path):
    """Downloads a video from a URL to a file.

    Args:
        url: The URL of the video to download.
        output_file_path: The path to the file where the video will be saved.
    """
    try:
        import requests
        logger.info("_Video Downloading Started")
        response = requests.get(url, stream=True)
        with open(output_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info("_Video Downloaded")
        return True
    except Exception as Err:
        logger.warning(f"Error in Download Video : {Err}")
        return False

def running_background(py_file_name:str,video_id:int,video_file_path:str,video_date:str,video_time:str):
    """Checking OS Version and Then Run in Background on According to Python3 or Python

    - If Any Error Occurs Code Exit
    - If No OS Found Then Exit

    Args:
        py_file_name (STR): Python File Name
        video_file_path (STR): Video File Path


    """
    try:
        logger.info('_Start Backgroung Process ')
        if sys.platform == 'win32':
            print('Running on Windows')
            logger.info('__Running On Windows')
            subprocess_run(["python", f"{py_file_name}",f"{video_id}", f"{video_file_path}",f"{video_date}",f"{video_time}","&"])
        elif sys.platform == 'linux':
            subprocess_run(["python3", f"{py_file_name}" ,f"{video_id}", f"{video_file_path}",f"{video_date}",f"{video_time}","&"])
            logger.info('__Running on Linux')
        elif sys.platform == 'darwin':
            logger.info('__Running on Mac')
            subprocess_run(["python3", f"{py_file_name}" ,f"{video_id}", f"{video_file_path}",f"{video_date}",f"{video_time}","&"])
        else: 
            logger.warning(f"OS Not Found {platform}")
            exit() #Code Exist
    except Exception as Err:
        logger.warning(f"Issue In Checking OS Error  {Err}")
        exit()
    finally:
        logger.info('_End Backgroung Process ')
def main():
    '''
    Check in DB's Table <Customer_id>_videos
    In Python : Query Execute
        To get the list of all rows[video_id,video_url] that COLUMN analyzed == False
    If No new videos found that means : No Videos Exist

        Continue

    If List_of_Video Found :
        Iterate a Loop of video
            each_video pass as parameter in function draw_boundry_box(video_id,video_url)
    
    '''
    logger.info(f'Code Executing Start')    
      # Folder 1 | frames Creation
    try:
        # Step 1 : | Start | Get the New Video List
        table_name=f'"argus"."1005_videos"'
        video_url=ArgusDB().get_columns(table_name=table_name,columns=["video_id"," url","camera_id"],where=f'''analyzed = false and camera_id = 'Cam3' and under_analysis=0''', extra=' ORDER BY video_id DESC LIMIT 1')
        logger.info("_Get UnProcessed Video From DB")
        # Step 1 : | End |
        
        # print(f"Total Video",len(video_url))
        logger.info(f"_Total UnProcess Video Are : {len(video_url)} ")
        for each_video in video_url:
            # Step 2 : | Start | Download The Each Video
            logger.info(f"Each Video And Apply Algo")
            print(each_video)                   
            video_id=int(each_video[0])
        
            # print("Downloading Video")
            video_url=each_video[1].replace('dl=0','dl=1')
            video_time_stamp=''
            try:
                # Extracting TimeStamp from Video
                video_time_stamp=video_url.split('/')[6]
                video_time_stamp=video_time_stamp.split('.')[0]
                video_time_stamp=video_time_stamp[4:]
            except Exception as E:
                logger.info(f"Issue in Video TimeStamp {E}")
            file_name=f'{each_video[2]}_{video_time_stamp}_{video_id}_video.mp4'
            # file_name=  Cam3__2023_12_25__08_41_39671_video.mp4
            logger.info(f"_Video Name Started : {file_name}")
            logger.info(f'{device_video_path}{file_name}')
            status_downloading = download_video(video_url,f'{device_video_path}{file_name}')
            ArgusDB().update_query_where(
                table_name=table_name,
                columns={ 'under_analysis' : SERVER_ID },
                where_condition=f''' video_id = {video_id} '''
            )
            logger.info(f"__Download Video : {file_name} - {status_downloading}")

            video_file_path=f'{device_video_path}{file_name}'
    
            #################### Running Code On Backrgound ########################
            date_int=0
            time_int=0
            date_int=video_time_stamp.replace('_','') #_2023_12_25__08_41_
            time_int=int(date_int[8:]+'00')
            date_int=int(date_int[:8])
            print("video",time_int,date_int)
            running_background(py_file_name=f"{basedir}/analysis_with_area.py",video_file_path=video_file_path,video_id=video_id,video_date=date_int,video_time=time_int)
            logger.info('Run Video subprocess')
            



            """
            # Step 2 : | End | Download The Each Video
            if status_downloading:
                #Step 3 : | Start |  Apply Algo 
                # logger.info(f'_Downloaded Video : {each_video}')
    
    
                
                # logger.info('_Algo Executing python3 /home/paperspace/argus-ganecos-backend1/cam2_algo.py {each_video[0]} &')
                # os.system(f'python3 /home/paperspace/argus-ganecos-backend1/cam2_algo.py {each_video[2]}{each_video[0]} ')
                # if  each_video[2] in ['Cam1','Cam2']:
                #     cam1_filter(file_name)
                # else:
                #     print('\n\nNot a Cam1 & Cam2')
                logger.info(f"__Apply Filter : {file_name}")
                status_filter=cam1_filter(file_name)    
                # print(status_filter)
                logger.info(f"__Apply Filter Done Filter_Status  : {status_filter}")
                if status_filter == False:
                    print("*"*10)
                    print("Issue In Cam1_filter or DB_Incident_ID")
                    print("*"*10)
                    logger.debug("Issue In Cam1_filter or DB")
                    return
                #Step 3 : | End |  Apply Algo 
                
                # Step 4 | Start | Uploaded Incident into DB
                print('DB Operation Startion')
                updation=ArgusDB().update_query_where(table_name=table_name,columns={'analyzed':'true'},where_condition=f'video_id={video_id}')
                logger.info(f"__Inserting into DB Video Analyzing Status : {updation} Video_id : {video_id}  Video_Name : {file_name} ")
                logger.info(f'_Video Name Done {file_name}')
                # Delete Video Start
                try:
                    full_video_path=f'{device_video_path}{file_name}'
                    logger.info(f'Deleting File {full_video_path}')
                    if os.path.isfile(full_video_path):
                        os.remove(full_video_path)
                        logger.info(f'File Deleted Done {full_video_path}')
                except Exception as E:
                    logger.debug(E)
                    logger.debug(f'Issue is Delete File : {full_video_path}')
                
                print(f"Update Incident ID Status : {updation}")
                
                # Delete Video End
            """
    except Exception as E:
        logger.warning(f"Issue in main() : {E}")   
        logger.exception("Issue In Main Function ")        
    
    finally:
        logger.info(f'Code Executing End')    
        return 
        


if __name__ == '__main__':
    
    while True:
        main()