from io import BytesIO
import boto3,requests

client=boto3.client('s3')
buck=input("Enter the name of the bucket: ")
url=input("Enter the url you want to host: ")

# create bucket
def createBucket(buck):
    try:
        response=client.create_bucket( 
                    Bucket=f"{buck}", 
                    CreateBucketConfiguration={'LocationConstraint':'ap-south-1'}, 
                    ObjectLockEnabledForBucket=False, 
                    ObjectOwnership='BucketOwnerPreferred'
                    )
    except Exception as e:
        print(e)

# with open("D:/vscode/boto/s3/pic/Cafe-Owners.png", "rb") as image2string: 
#     converted_string = base64.b64encode(image2string.read()) 

# getting content
def conte():
    response=requests.get(url)
    return response.content


# upload objects
# Use base64 to convert html file/img ---> string
def uploadFiles(buck):
    try:
        # hostName=input("Enter the host name: ")
        content=conte()
        response=client.put_object(
            ACL='public-read',
            Bucket=f'{buck}',
            Body=BytesIO(content),
            Key='index.html',
            ContentType='html'
        )
        print("Object uploaded successfully...")
    except Exception as e:
        print(e)
# make public acl
def acl(buck):
    try:
        response=client.put_bucket_acl(
            Bucket=f"{buck}",
            ACL="public-read"
        )
        print("ACL is set to public...")
        # print(response)
    except Exception as e:
        print(e)

# unblock public access
def publicAccessBlock(buck):
    try:
        response=client.put_public_access_block(
            Bucket=f"{buck}",
            PublicAccessBlockConfiguration ={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
            }
        )
        print("Unblocked BlockPublicAccess...")
    except Exception as e:
        print(e)

# enable static website hosting
def staticHost(buck):
    try:
        response=client.put_bucket_website(
            Bucket=f"{buck}",
            WebsiteConfiguration={
                'IndexDocument':{
                    'Suffix':'index.html'
                },
                'ErrorDocument':{
                    'Key':'error.html'
                }
            }
        )
        print("Static website hosting enabled...")
    except Exception as e:
        print(e)

# List buckets
def listBuckets():
    response=client.list_buckets()
    return response

def listObject(buck):
    response=client.list_objects(
        Bucket=f"{buck}",
        # MaxKeys=2
    )
    return response

# Delete Buckets
def deleteBucket(buck):
    try:
        response=client.delete_bucket(
            Bucket=f"{buck}"
        )
    except Exception as e:
        print(e)

# empty Buckets
def emptyBucket(buck,key):
    response=client.delete_objects(
        Bucket=f"{buck}",
        Delete={
            'Objects':[
                {
                    'Key':f"{key}"
                },
            ],
        }
    )

def scrap():
    response=requests.get(url)
    data=response.text
    with open('index.html','w',encoding='utf-8') as file:
        file.write(data)

# static website hosting
def staticWebHost(buck):
    publicAccessBlock(buck)
    acl(buck)
    conte()
    uploadFiles(buck)
    # scrap()
    staticHost(buck)

# obj=listObject(buck)
# sizeO=0
# for i in obj['Contents']:
#     sizeO+=1
# for i in range(0,sizeO):
#     print(obj['Contents'][i]['Key'])

list=listBuckets()
# print(list)
# print(list['Buckets'][0]['Name'])
size=0
flag=0
for i in list['Buckets']:
    size+=1
# print(size)
for i in range(0,size):
    if buck==list['Buckets'][i]['Name']:
        flag=1
print(flag)
if flag==1:
    obj=listObject(buck)
    sizeO=0
    # print(obj)
    for i in obj['Contents']:
        sizeO+=1
    for i in range(0,sizeO):
        key=obj['Contents'][i]['Key']
        emptyBucket(buck,key)
    print("Emptying Bucket...")
    print("deleting bucket....")
    deleteBucket(buck)
    print("creating bucket....")
    createBucket(buck)
    staticWebHost(buck)
else:
    print("creating bucket....")
    createBucket(buck)
    staticWebHost(buck)
print(f"Go to this link to vist your website ==> http://{buck}.s3-website.ap-south-1.amazonaws.com ")