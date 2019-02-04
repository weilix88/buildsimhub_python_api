import pandas as pd
from datetime import datetime as dt
import logging


def process_data_given_unit(input_file_name, output_file_name, quantity, calculate_method):
    start_time = dt.now()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler('calculate.log')
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info('Function entered')
    
    df = pd.read_csv(input_file_name)
    logger.info('Read user input successfully')
    if quantity > 60:
        logger.info('The timerange you give is too large')
        raise Exception('The timerange you give is too large')
    elif 60 % quantity != 0:
        logger.info('The timerange you give cannot be divided evenly')
        raise Exception('The timerange you give cannot be divided evenly')
    elif quantity == 60:   
        date_dict = dict()
        row_fields = df.keys()
        for index, row in df.iterrows():
            date_str = row[row_fields[0]]
            date_obj = dt.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            date_result = dt.strftime(date_obj, '%m/%d/%Y %H')
            if date_result not in date_dict:
                date_dict[date_result] = dict()
                for i in range(1, len(row_fields)):
                    date_dict[date_result][row_fields[i]] = []
    
            for i in range(1, len(row_fields)):
                date_dict[date_result][row_fields[i]].append(row[row_fields[i]])
    
        export_row_fields = list()
        export_row_fields.append('timeStamp')
        export_row_fields.extend(row_fields[1:])
        export_df = pd.DataFrame(columns = export_row_fields)
        row = 0
        for key, value in date_dict.items():
            tempList = [key+':00']
            for i in range(1, len(export_row_fields)):
                l1 = value[export_row_fields[i]]
                if calculate_method == 'sum':
                    result = sum(l1)
                elif calculate_method == 'average':
                    result = sum(l1)/float(len(l1))
                else:
                    logger.info('Your operation is not defined in our system')
                    raise Exception('Your operation is not defined in our system')
                tempList.append(result)
        
            export_df.loc[row] = tempList
            row = row+1

        export_df.to_csv(output_file_name)
    
    else:
        minRange = list()
        for i in range(int(60/quantity)):
            minRange.insert(0, quantity*i)
            
        date_dict = dict()
        row_fields = df.keys()
        for index, row in df.iterrows():
            date_str = row[row_fields[0]]
            date_obj = dt.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            date_result = dt.strftime(date_obj, '%m/%d/%Y %H:%M')
            date_hour = date_result[:-3]
            date_min = date_result[-2:]
            date_min_range = 0
            for j in range(len(minRange)):
                if int(date_min) >= minRange[j]:
                    date_min_range = minRange[j]
                    break
            
            if date_hour not in date_dict:
                date_dict[date_hour] = dict()
            
            if date_min_range not in date_dict[date_hour]:
                date_dict[date_hour][date_min_range] = dict()
                for i in range(1, len(row_fields)):
                    date_dict[date_hour][date_min_range][row_fields[i]] = []
    
            for i in range(1, len(row_fields)):
                date_dict[date_hour][date_min_range][row_fields[i]].append(row[row_fields[i]])
                    #print (date_dict[date_hour].keys())
    
        export_row_fields = list()
        export_row_fields.append('timeStamp')
        export_row_fields.extend(row_fields[1:])
        export_df = pd.DataFrame(columns = export_row_fields)
        row = 0
        for hour, min_dict in date_dict.items():
            for minutes, value in min_dict.items():
                #print(minutes)
                minutes_str = str(minutes)
                if len(minutes_str) == 1:
                    minutes_str = '0' + minutes_str
                tempList = [hour+':'+minutes_str]

                for i in range(1, len(export_row_fields)):
                    l1 = value[export_row_fields[i]]
                    if calculate_method == 'sum':
                        result = sum(l1)
                    elif calculate_method == 'average':
                        result = sum(l1)/float(len(l1))
                    else:
                        logger.info('Your operation is not defined in our system')
                        raise Exception('Your operation is not defined in our system')
                    tempList.append(result)
        
                export_df.loc[row] = tempList
                row = row+1

        export_df.to_csv(output_file_name)
    
    end_time = dt.now()
    logger.info('Output File is generated and saved')
    logger.info('Totol Data is %d', len(df))
    logger.info('Total Time for the task is %d', (end_time - start_time).total_seconds())
    logger.info('Current Resolution %d', 1)
    logger.info('Converted Resolution %d', quantity)


def main():
    process_data_given_unit('pow_lighting_raw.csv', 'result.csv', 12, 'sum')


main()