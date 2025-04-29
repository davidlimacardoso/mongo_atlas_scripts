
# Create the cloud provider access role

```
curl --user "PUB_KEY:PRIV_KEY" --digest \
 --header "Content-Type: application/json" \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --include \
 --request POST "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/cloudProviderAccess?pretty=true" \
 --data '
 {
 "providerName": "AWS"
 }'
 
 ###########
 {
  "atlasAWSAccountArn" : "arn:aws:iam::50000xxx0x00:root",
  "atlasAssumedRoleExternalId" : "xxxxxxxx-3edb-43da-90af-xxxxxxxxxxxx",
  "authorizedDate" : null,
  "createdDate" : "2025-04-18T16:26:49Z",
  "featureUsages" : [ ],
  "iamAssumedRoleArn" : null,
  "providerName" : "AWS",
  "roleId" : "68027d4945cdf62xxxxxxxxx"
}
```

# Return all the cloud provider access roles
```
curl --user "PUB_KEY:PRIV_KEY" --digest \
 --header "Content-Type: application/json" \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --include \
 --request GET "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/cloudProviderAccess?pretty=true"
 ```
 
 #################
 
 ##  Criei a role ame-atlas-export-backup-to-s3_role
 ```
curl --user "PUB_KEY:PRIV_KEY" --digest \
 --header "Content-Type: application/json" \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --include \
 --request PATCH "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/cloudProviderAccess/68027d4945cdf62xxxxxxxxx" \
 --data '
 {
 "providerName": "AWS",
 "iamAssumedRoleArn": "arn:aws:iam::355315421281:role/ame-atlas-export-backup-to-s3_role"
 ```
 
 ##############
 
 # Create the object S3 bucket
 ```
curl --user "PUB_KEY:PRIV_KEY" --digest \
 --header "Content-Type: application/json" \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --include \
 --request POST "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/backup/exportBuckets?pretty=true" \
 --data '
 {
 "bucketName": "ame-mongo-atlas-backups-exported",
 "cloudProvider": "AWS",
 "iamRoleId": "68027d4945cdf62xxxxxxxxx"
 }'
```
#############
# Return all AWS S3 buckets used for the cloud backup snapshot exports
```
curl --user "PUB_KEY:PRIV_KEY" --digest \
 --header "Content-Type: application/json" \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --include \
 --request GET "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/backup/exportBuckets?pretty=true"
 ```
############

# Export policy
```
curl --user "PUB_KEY:PRIV_KEY" --digest --include \
 --header "Accept: application/json" \
 --header "Content-Type: application/json" \
--request PATCH "https://cloud.mongodb.com/api/atlas/v1.0/groups/99bee66bf642ff5xxxxxxxxx/clusters/jupter-prd-mongodb-byebye/backup/schedule" \
--data '{
  "autoExportEnabled": true,
  "export": {
    "exportBucketId": "6802bb714a542f77xxxxxxxx",
    "frequencyType": "daily"
  },
  "referenceHourOfDay": 0,
  "referenceMinuteOfHour": 55,
  "updateSnapshots": true
}'
```

#################################
## Return all Snapshot Export Jobs
```
curl --user "PUB_KEY:PRIV_KEY" --digest --include \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --request GET "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/clusters/jupter-prd-mongodb-byebye/backup/exports"
```
#########################################################################
 
 
 EXPORT MANUAL 
 ########################################################################
 ### EXPORT BACKUP PARA O S3 ###
 ```
curl --user "PUB_KEY:PRIV_KEY" --digest \
 --header "Content-Type: application/json" \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --include \
 --request POST "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/clusters/jupter-prd-mongodb-byebye/backup/exports" \
 --data '
 {
  "customData": [
   {
    "key": "exported",
    "value": "desmob"
   }
  ],
  "exportBucketId": "6802bb714a542f77xxxxxxxx",
  "snapshotId": "67ea1a511d21887c425133c2"
}'
# RETORNO 
{"createdAt":"2025-04-19T09:49:13Z","customData":[],"exportBucketId":"6802bb714a542f77xxxxxxxx","exportStatus":{"exportedCollections":0,"totalCollections":0},"id":"680371990afbe35fcb5e7ca6","prefix":"exported_snapshots/5aeb8f4896e82136bd0f229f/99bee66bf642ff5xxxxxxxxx/jupter-prd-mongodb-byebye/2025-03-31T0434/1745056152","snapshotId":"67ea1a511d21887c425133c2","state":"Queued"}
```

# VIRIFICA O STATUS DE EXPORTAÇÃO
### USE O EXPORT ID DO STEP ANTERIOR
```
curl --user "PUB_KEY:PRIV_KEY" --digest --include \
 --header "Accept: application/vnd.atlas.2025-03-12+json" \
 --request GET "https://cloud.mongodb.com/api/atlas/v2/groups/99bee66bf642ff5xxxxxxxxx/clusters/jupter-prd-mongodb-byebye/backup/exports/680371990afbe35fcb5e7ca6"

# Retorno
{"createdAt":"2025-04-19T09:49:13Z","customData":[],"exportBucketId":"6802bb714a542f77xxxxxxxx","exportStatus":{"exportedCollections":105,"totalCollections":105},"id":"680371990afbe35fcb5e7ca6","prefix":"exported_snapshots/5aeb8f4896e82136bd0f229f/99bee66bf642ff5xxxxxxxxx/jupter-prd-mongodb-byebye/2025-03-31T0434/1745056152","snapshotId":"67ea1a511d21887c425133c2","state":"InProgress"}
```
