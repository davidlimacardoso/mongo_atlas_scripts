#!/bin/bash

regex='/(.+)/(.+)/.+'
dir=${1%/}
connstr=$2

# iterate through the subdirectories of the downloaded and
# extracted snapshot export and restore the docs with mongoimport
find $dir -type f -not -path '*/\.*' -not -path '*metadata\.json' | while read line ; do
  [[ $line =~ $regex ]]
  db_name=${BASH_REMATCH[1]}
  col_name=${BASH_REMATCH[2]}
  mongoimport --uri "$connstr" --mode=upsert -d $db_name -c $col_name --file $line --type json
done

# create the required directory structure and copy/rename files
# as needed for mongorestore to rebuild indexes on the collections
# from exported snapshot metadata files and feed them to mongorestore
find $dir -type f -name '*metadata\.json' | while read line ; do
  [[ $line =~ $regex ]]
  db_name=${BASH_REMATCH[1]}
  col_name=${BASH_REMATCH[2]}
  mkdir -p ${dir}/metadata/${db_name}/
  cp $line ${dir}/metadata/${db_name}/${col_name}.metadata.json
done
mongorestore "$connstr" ${dir}/metadata/

# remove the metadata directory because we do not need it anymore and this returns
# the snapshot directory in an identical state as it was prior to the import
rm -rf ${dir}/metadata/
