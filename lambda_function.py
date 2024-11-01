import urllib
import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    jpg_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    split_key = jpg_key.split('.')
    root = split_key[0]
    png_key = root + ".png"
    bmp_key = root + ".bmp"
    gif_key = root + ".gif"
    jpg_object = s3.get_object(Bucket=bucket_name, Key=jpg_key)
    jpg_data = jpg_object['Body'].read()

    with Image.open(io.BytesIO(jpg_data)) as image:
        png_buffer = io.BytesIO()
        image.save(png_buffer, format="PNG")
        png_buffer.seek(0)

    with Image.open(io.BytesIO(jpg_data)) as image:
        bmp_buffer = io.BytesIO()
        image.save(bmp_buffer, format="BMP")
        bmp_buffer.seek(0)

    with Image.open(io.BytesIO(jpg_data)) as image:
        gif_buffer = io.BytesIO()
        image.save(gif_buffer, format="GIF")
        gif_buffer.seek(0)

    s3.put_object(Bucket=bucket_name, Key=png_key, Body=png_buffer, ContentType='image/png')
    s3.put_object(Bucket=bucket_name, Key=bmp_key, Body=bmp_buffer, ContentType='image/bmp')
    s3.put_object(Bucket=bucket_name, Key=gif_key, Body=gif_buffer, ContentType='image/jpg')

    return {
        'statusCode': 200,
        'body': f"Converted {jpg_key} and uploaded to {bucket_name}"
    }
