from flask import Flask,render_template,request
import boto3
app = Flask(__name__)
_BUCKET_NAME = '1367-sugumar-b1'
client = boto3.client('s3')

def get_folders(bucket_name):
    response = client.list_objects_v2(Bucket=bucket_name, Prefix='', Delimiter='/')
    for content in response.get('CommonPrefixes', []):
        yield content.get('Prefix')
		
		
def get_files(prefix):
    file_list = []
    response = client.list_objects(Bucket=_BUCKET_NAME, Prefix=prefix)
    for content in response.get('Contents', []):
        file_list.append(content.get('Key'))
    return file_list


@app.route('/')
def home():
    folders = get_folders(_BUCKET_NAME)
    return render_template('home.html', folders=folders)

@app.route('/list_files')
def list_files():
    files = get_files(request.args.get('prefix' , ''))
    return ''.join(files[1:])

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8085)
