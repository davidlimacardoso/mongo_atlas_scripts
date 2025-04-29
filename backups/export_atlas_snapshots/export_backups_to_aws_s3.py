import requests
from requests.auth import HTTPDigestAuth

# Documentação de Referência
    #https://www.mongodb.com/pt-br/docs/atlas/reference/api-resources-spec/v2/2023-11-15/#tag/Cloud-Backups/operation/createBackupExportJob
    #https://medium.com/globant/export-your-mongodb-snapshots-with-the-atlas-administration-api-7c39ac38eb9c


# Suas credenciais e informações
PUBLIC_KEY = "XXXXXXXX"
PRIVATE_KEY = "XXXXXXXX"
PROJECT_ID = "60bee66bf642akjsdawdasda"
BASE_URL = "https://cloud.mongodb.com/api/atlas/v2"

def get_projects_and_clusters(PUBLIC_KEY, PRIVATE_KEY):
    """
    Obtém a lista de projetos e clusters disponíveis.
    """
    url = f"{BASE_URL}/clusters"
    headers = {"Accept": "application/vnd.atlas.2025-03-12+json"}
    response = requests.get(f"{url}", headers=headers, auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY))

    projects_collection = []

    if response.status_code == 200:
        projects = response.json().get("results", [])
        # print("Projetos e Clusters disponíveis:")
        for project in projects:
            projects_collection.append({'name': project['groupName'], 'id': project['groupId']})
            
            for cluster in project["clusters"]:
                projects_collection[-1].setdefault('clusters', []).append(cluster['name'])

    else:
        print(f"Erro ao obter projetos e clusters: {response.status_code} - {response.text}")

    return projects_collection

def get_snapshots(public_key, private_key, project_id, cluster_name):
    """
    Obtém a lista de snapshots para um determinado cluster.
    """
    url = f"{BASE_URL}/groups/{project_id}/clusters/{cluster_name}/backup/snapshots"
    headers = {"Accept": "application/vnd.atlas.2025-03-12+json"}
    response = requests.get(url, headers=headers, auth=HTTPDigestAuth(public_key, private_key))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter snapshots: {response.status_code} - {response.text}")
        return None

def export_snapshots_to_s3(group_id, cluster_name, snapshot_id, export_bucket_id, public_key, private_key):
    """
    Exporta os snapshots para um bucket S3.
    """
    url = f"{BASE_URL}/groups/{group_id}/clusters/{cluster_name}/backup/exports"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.atlas.2025-03-12+json"
    }
    payload = {
        "customData": [
            {
                "key": "exported",
                "value": "desmob"
            }
        ],
        "exportBucketId": export_bucket_id,
        "snapshotId": snapshot_id
    }
    response = requests.post(
        url,
        headers=headers,
        auth=HTTPDigestAuth(public_key, private_key),
        json=payload
    )
    if response.status_code == 200:
        print("Exportação iniciada com sucesso.")
        return response.json()
    else:
        print(f"Erro ao exportar snapshot: {response.status_code} - {response.text}")
        return None

def main():
    export_bucket_id = "xxxxxxxxxxxxxxxx"  # ID do bucket S3 para exportação
    # Obtém a lista de projetos e clusters
    project_clusters = get_projects_and_clusters(PUBLIC_KEY, PRIVATE_KEY)

    for project in project_clusters:
        if 'clusters' in project:
            print(f"Projeto: {project['name']}, ID: {project['id']}")
            for cluster in project['clusters']:
                print(f"  Cluster: {cluster}")

                snapshots_data = get_snapshots(PUBLIC_KEY, PRIVATE_KEY, project['id'], cluster)
                
                if snapshots_data and "results" in snapshots_data:
                    snapshots = snapshots_data["results"]
                    if snapshots:
                        latest_snapshot = max(snapshots, key=lambda s: s["createdAt"])
                    else:
                        latest_snapshot = None
                else:
                    latest_snapshot = None
                
                if latest_snapshot:
                    export_snapshots_to_s3(
                        project['id'],
                        cluster,
                        latest_snapshot['id'],
                        export_bucket_id,
                        PUBLIC_KEY,
                        PRIVATE_KEY
                    )


    else:
        print("Não foram encontrados snapshots.")

if __name__ == "__main__":
    main()
