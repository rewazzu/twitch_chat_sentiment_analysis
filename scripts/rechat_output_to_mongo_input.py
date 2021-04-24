'''
This file takes in a json that is given by rechat and then outputs a csv that is appropriate for our use.
'''

import json
import pandas as pd
import datetime
import dateutil.parser
import math
#load file
file_name = r"C:\Users\Hamza\Documents\OMSCS\DVA\Project\Chat JSON\330639009.json"
data = open(file_name, encoding='utf-8-sig')
json_data = json.load(data)
df = pd.DataFrame(json_data)
#get vod id
vod_id = file_name.split('\\')[-1][:-5]

#flatten data
message_dict_frame = df.message.apply(pd.Series)
df = df.join(message_dict_frame)
commenter_dict_frame = df.commenter.apply(pd.Series)
df['user_id'] = commenter_dict_frame['_id']
df['user_name'] = commenter_dict_frame['display_name']
df['vod_id'] = vod_id

#convert timestamp to datetime
timestamp = df.created_at[0]
timestamp_datetime = datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%fZ")
df['Timestamp'] = df.created_at.apply(lambda x: dateutil.parser.parse(x))
#create bins
df['Bin'] = df.content_offset_seconds.apply(lambda x: math.floor(x/10))

#format output dataframe
output = pd.DataFrame()
output['Vod_id'] = df['vod_id']
output['Timestamp'] = df['Timestamp']
output['Content_offset_seconds'] = df['content_offset_seconds']
output['Bin'] = df['Bin']
output['Username'] = df['user_name']
output['User_id'] = df['user_id']
output['Message'] = df['body']
output['Emoticons'] = df['emoticons']
#output_csv = output.to_csv('test.csv')
output_path = str(vod_id) + '_formatted.json'
output_json = output.to_json(output_path, orient='records')


