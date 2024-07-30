import datetime
import pytz


def ist_time():
    ist_time = ''
    try:
        ist_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    except:
        print("Issue in timezone")

        # return False
    return ist_time


def get_IST_current_Hour_and_Min() -> str:
    """ This Calculate the Current India Standard Time 
        Hour : Minutes and Return 

    Returns:
        str: HH:MM
    """
    ist = ist_time()
    ist_time_formatted = ist.strftime("%H:%M")
    # print(ist_time_formatted)

    return ist_time_formatted

def get_IST_current_time_now() -> str:
    """Return YYYY/MM/DD HH:MM
    """
    ist = ist_time().strftime('%Y/%m/%d %H:%M')
    
    
    return ist
    

def get_IST_today_date():
    """ This Calculate the Current India Standard Time 
        Hour : Minutes and Return 

    Returns:
        str: HH:MM
    """
    ist = ist_time()
    # print(ist)
    ist_time_formatted = ist.strftime("%Y/%m/%d")
    # print(ist_time_formatted)

    return ist_time_formatted

def get_today_day():
    """This Calculate the India Standard Time
        Current day
    """
    ist=ist_time().strftime('%A').lower()
    print(ist)
    return ist

def cal_thershold_time(time_in_HH_MM,thershold_time_HH_MM):
    try:
        
        import datetime
        time_delta=datetime.timedelta(minutes=int(thershold_time_HH_MM))
        datetime_object = datetime.datetime.strptime(time_in_HH_MM, '%H:%M')
        calc_entry_thershold=time_delta+datetime_object
        print(time_in_HH_MM)
        calc_entry_thershold=str(calc_entry_thershold.strftime("%H:%M"))
        print('calc_entry_thershold',calc_entry_thershold)
        
    except Exception as E:
        print(E)
        return 'False'
    return calc_entry_thershold

if __name__ == '__main__':
    # print(get_IST_today_date())
    # print(get_today_day())
    print(get_IST_current_time_now())
    