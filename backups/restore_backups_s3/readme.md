### Doc. de Referência
[Importar arquivo do S3](https://www.mongodb.com/pt-br/docs/atlas/backup/cloud-backup/import-archive/?msockid=364638f4f8b7660e24382d28f9ac6767)


## Baixar Objeto de Backup
Copie os dados no bucket S3 para uma pasta usando a do Amazon Web Services CLI e extraia os dados.
```bash
aws s3 cp s3://ame-mongo-atlas-backups/exported_snapshots/5aeb8f4896e8xxxxxxxxxx/60bee66bf642ff5xxxxx/jupter-prd-mylorem/2021-12-31T1634/1745349244/ mybucket --recursive
gunzip -r mybucket
```

## Criar Script massimport.sh
Copie e armazene o seguinte script em um arquivo denominado massimport.sh.

```sh
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
```
--mode=upsert permite que mongoimport lide com documentos duplicados de um arquivo.

--uri especifica a connection string para o Atlas cluster.

## Executar Script
Execute a utilidade massimport.sh para importar os dados arquivados no cluster Atlas.

```bash
sh massimport.sh mybucket "mongodb+srv://127.0.0.1:27017"
``


## Validar Collections


- show databases

- use db_mylorem

- show collections()

- db.db_mylorem.find()
