import boto3

ec2=boto3.client('ec2',region_name='ap-south-1')

def listInstance():
    response=ec2.describe_instances()
    return response
    # print(response)
def createInstance():
    try:
        response=ec2.run_instances(
            ImageId='ami-05295b6e6c790593e',
            InstanceType='t2.micro',
            KeyName='mumkey',
            MinCount=1,
            MaxCount=1
        )
        print("Instance has been created...")
    except Exception as e:
        print(e)

def startInstance(id):
    try:
        response=ec2.start_instances(
            InstanceIds=[id]
        )
        print("Instance has been started...")
    except Exception as e:
        print(e)

def stopInstance(id):
    try:
        response=ec2.stop_instances(
            InstanceIds=[id]
        )
        print("Instance has been stopped...")
    except Exception as e:
        print(e)
        
def terminateInstance(id):
    try:
        response=ec2.terminate_instances(
            InstanceIds=[id]
        )
        print("Instance has been terminated...")
    except Exception as e:
        print(e)

def operation():
    res=listInstance()
    count=0
    for i in res['Reservations']:
        print(i)
        count+=1
    # print(count)

    while True:
        try:
            for i in range(count):
                InstanceId=res['Reservations'][i]['Instances'][0]['InstanceId']
                print(f"{i}) {InstanceId}")
            Id=int(input("Choose the instance Id to perform operations: "))
            InstanceId=res['Reservations'][Id]['Instances'][0]['InstanceId']
            opt=input("1) start instance \n2) stop instance \n3) terminate \n4) If you need to exit.. -----> ")
            if opt=='1':
                startInstance(InstanceId)
            elif opt=='2':
                stopInstance(InstanceId)
            elif opt=='3':
                terminateInstance(InstanceId)
            elif opt=='4':
                break
            else:
                print("Enter a valid option...")
        except Exception as e:
            print(e)

while True:
    try:
        oper=input("1) Create instance \n2) Do operation on the instances \n3) If you need to exit.. ----> ")
        if oper=='1':
            createInstance()
        elif oper=='2':
            operation()
        elif oper=='3':
            break
        else:
            print("Please Enter a valid input...")
    except Exception as e:
        print(e)
