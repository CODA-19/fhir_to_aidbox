#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 12:16:59 2021

 The example uploads a file to the Minio present in a VM.
 
 It then creates a URL and uses it to upload the file on
 the Aidbox.
 
 
 Please provide the key inputs to Minio

@author: rdas
"""


import os
import requests
import requests.auth
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import logging 








def establish_minio_connect():
    
   """
    
    This method establishes the connection with Minio through the use
    of boto3.
    
    aws_access_key_id = "From the Minio key file (secret)"
    aws_secret_access_key = "From the Minio key file (secret)"
    
   """
    
   
    
   sboto = boto3.resource('s3',aws_access_key_id = '', aws_secret_access_key = '', endpoint_url='http://recherche-coda19-rouge:9000',\
                   config=Config(signature_version='s3v4'))
   
   
   return sboto


def upload_file_minio(s3,filename):

   """
    
     This method uploads a file to a specified bucket in the Minio
     
     It is assumed here that the Minio has a bucket by the name
     chumtestbucket. Plus the file to be fetched and uploaded will
     have the names filename, and filename
     respectively (same names)
     
     It is assumed here that the file that is being fetched is in the working
     directory of the user.
     
     The location of the file in the Minio would be chumtestbucket/filename
     in the present case.
     
     Input argument: s3 type object
                     filename type string
     Return: None.

   """
   
   

   s3.Bucket('chumtestbucket').upload_file(filename,filename)
   
   
   
   
 
def create_presigned_url(bucket_name, object_name, expiration=3600):
   
    """
     Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    
    
    Kept the connection separate here.
    
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', endpoint_url='http://recherche-coda19-rouge:9000',aws_access_key_id = '', aws_secret_access_key = '')
    
    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': object_name}, ExpiresIn=expiration)
    
    except ClientError as e:
    
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response






# Program entry
if __name__ == "__main__":
    
    
    
    ## Only the file, assuming the file is present in the working directory
    
    
    filetoupload = 'abc.ndjson.gz'

    
    ## Establish the connection with Minio 
    
    s3 = establish_minio_connect()
    
    
    ## Upload files to the Minio
    
    upload_file_minio(s3, filetoupload)
    
    
    ## Call the create url function by providing the name of the bucket in Minio and the desired
    ## file.
    
    url = create_presigned_url('chumtestbucket',filetoupload)
    
    ## Create the payload
    
    payload=({"source":url})
    
    
    ## Perform the user authorization
    ## Basic authorization settings described by python_load_script was performed earlier in the Aidbox.
    ## To nkow more refer to https://docs.aidbox.app/user-management-1/auth/basic-auth
    
    requests.get("http://recherche-coda19-orange:8888/User", auth=requests.auth.HTTPBasicAuth('load_script','hello123'))
    
    
    ## Perform the upload task to the Aidbox.
    
    requests.post("http://recherche-coda19-orange:8888/fhir/$load",auth=requests.auth.HTTPBasicAuth('load_script','hello123'),json=payload)

    
   
  
    
