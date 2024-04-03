import boto3

client=boto3.client('s3')
def listBuckets():
    response=client.list_buckets()
    # print(response['Buckets'])
    return response['Buckets']

def createBucket():
    response=client.create_bucket(
        Bucket='plastic-vali1232',
        CreateBucketConfiguration={
            'LocationConstraint':'ap-south-1'
        }
    )
    print(response)

def uploadFileS3():
    filepath="D:/vscode/boto/pic"
    response=client.upload_file(filepath,'plastic-vali1232',"pic")
    print(response)

def deleteObject():
    response=client.delete_object(
        Bucket='plastic-vali1232',
        Key='Cup-of-Hot-Chocolate.png'
    )
    print(response)

# createBucket()
# listBuckets()
# uploadFileS3()
# deleteObject()