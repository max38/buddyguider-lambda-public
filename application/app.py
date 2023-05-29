import boto3


client = boto3.resource('dynamodb')



# def lambda_request_suggestion_handler(event, context):
    # request_payload = json.loads(event['body'])
    

    # chatgpt_response = ask_chatgpt(city=request_payload['city'], days=request_payload['days'])
    # suggest_places = chatgpt_response['choices'][0]['message']['content']
    # suggest_places = json.loads(suggest_places)
    
    # for day in suggest_places:
    #     for place in suggest_places[day]:
    #         update_location(place)
    
    # return {
    #     'statusCode': 200,
    #     'body': {'arn': SNS_BUDDYGUIDER_REQUEST_SUGGESTION_ARN}
    #     # 'body': suggest_places
    # }




# def pushish_message_to_sns(message):
#     sns = boto3.client('sns')
#     sns.publish(
#         TopicArn='arn:aws:sns:ap-southeast-1:123456789012:tripz-pushish',
#         Message=message
#     )
    

def update_location(data):
    location_table = client.Table("tripz_location")
    
    location_slug = f"{data['country_name']}-{data['province']}-{data['place_name']}".lower().replace(" ", "")
    
    # location_table_info = location_table.get_item(Key={'location_slug': location_slug})
    
    # if 'Item' in location_table_info:
    #   pass
    # else:
    #     insert_data = {
    #         'id': str(uuid.uuid4()),
    #         'location_slug': location_slug,
    #         'updated_timestamp': int(time.time()),
    #         'place_name': data['place_name'],
    #         'suggest_time_spend': data['suggest_time_spend'],
    #         'country_name': data['country_name'],
    #         'province': data['province'],
    #         'map_location': data['map_location'],
    #     }
        
    #     location_table.put_item(Item=insert_data)


# def ask_chatgpt(city=None, country=None, days=1):
#     chatgpt_activity_table = client.Table("tripz_chatgpt_activity")
#     # chatgpt_activity_info = chatgpt_activity_table.get_item(Key={'city': city, 'days': days})
    
#     # if 'Item' in chatgpt_activity_info:
#     #   pass
    
    
#     chatgpt_api_url = "https://api.openai.com/v1/chat/completions"
    # payload = {
    #   "model": "gpt-3.5-turbo",
    #   "temperature": 0.7,
    #   "messages": [{
    #       "role": "user", 
    #       "content": "Please give me a travel plan to visit " + city + " in " + str(days) + " days. and please return with json format like this ``` {\"day1\": [{\"activity\": \"...\", \"place_name\": \"...\", \"description\": \"...\", \"suggest_time_spend\": \"...\", \"country_name\": \"...\", \"province\": \"...\", \"map_location\": [\"lat\": \"..\", \"long\": \"..\"]}, {...}], \"day2\": [] } ```"
    #   }]
    # }
    
#     response = requests.post(chatgpt_api_url, headers={"Authorization": "Bearer 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"}, json=payload)
    
#     insert_data = {
#         'id': str(uuid.uuid4()),
#         'timestamp': int(time.time()),
#         'city': city,
#         'days': days,
#         'response': response.json()
#     }
    
#     chatgpt_activity_table.put_item(Item=insert_data)
    
#     return response.json()


