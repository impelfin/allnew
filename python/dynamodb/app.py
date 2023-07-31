import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table('st_info')

allData = table.scan()

print(allData['Items'])
