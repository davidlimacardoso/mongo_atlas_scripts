import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
from collections import defaultdict

PUBLIC_KEY = "XXXXXXXXXXXX"
PRIVATE_KEY = "XXXXXXXXXXX"
PROJECT_ID = "60bee66bf64asdawdasd"
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
    export_bucket_id = "6802bb714a5xxxxxxxxx"  # ID do bucket S3 para exportação
    project_clusters = get_projects_and_clusters(PUBLIC_KEY, PRIVATE_KEY)

    for project in project_clusters:
        if 'clusters' in project:
            print(f"Projeto: {project['name']}, ID: {project['id']}")
            for cluster in project['clusters']:
                print(f"  Cluster: {cluster}")

                snapshots_data = get_snapshots(PUBLIC_KEY, PRIVATE_KEY, project['id'], cluster)
                
                if snapshots_data and "results" in snapshots_data:
                    snapshots = snapshots_data["results"]
                    
                    if not snapshots:
                        print("  Não foram encontrados snapshots.")
                        continue

                    snapshots_by_year_month = defaultdict(list)

                    # IDs de snapshots a serem excluídos
                    exclude_snapshot_ids = ['67ea1a511d21887c425133c2', '67f2e273aa2b5f23c4bbaa70','67ea1a511d21887c425133c2','67f0aae4a5f73d5e433faab5','6807ca47115e6111f585c19e']

                    for snapshot in snapshots:

                        # Verifica se o snapshot já foi exportado
                        if snapshot['id'] in exclude_snapshot_ids:
                            print(f"  Ignorando snapshot: {snapshot['id']} pois já foi realizado o export")
                            continue

                        created_at = datetime.fromisoformat(snapshot["createdAt"][:-1])  # Remover 'Z'
                        year_month = (created_at.year, created_at.month)
                        snapshots_by_year_month[year_month].append(snapshot)

                    # Exportar snapshots para 2025 (último de cada mês)
                    for month in range(1, 13):
                        if (2025, month) in snapshots_by_year_month:
                            latest_snapshot = max(snapshots_by_year_month[(2025, month)], key=lambda s: s["createdAt"])
                            # print(project['id'], cluster, latest_snapshot['id'], latest_snapshot['createdAt'])
                            export_snapshots_to_s3(project['id'], cluster, latest_snapshot['id'], export_bucket_id, PUBLIC_KEY, PRIVATE_KEY)

                    # Exportar snapshots para 2024 (último de cada mês)
                    for month in range(1, 13):
                        if (2024, month) in snapshots_by_year_month:
                            latest_snapshot = max(snapshots_by_year_month[(2024, month)], key=lambda s: s["createdAt"])
                            # print(project['id'], cluster, latest_snapshot['id'], latest_snapshot['createdAt'])
                            export_snapshots_to_s3(project['id'], cluster, latest_snapshot['id'], export_bucket_id, PUBLIC_KEY, PRIVATE_KEY)

                    # Exportar snapshots para 2021-2023 (último de cada ano)
                    for year in range(2020, 2024):
                        if (year, 12) in snapshots_by_year_month:  # Considera janeiro como representante do ano
                            latest_snapshot = max(snapshots_by_year_month[(year, 12)], key=lambda s: s["createdAt"])
                            # print(project['id'], cluster, latest_snapshot['id'], latest_snapshot['createdAt'])
                            export_snapshots_to_s3(project['id'], cluster, latest_snapshot['id'], export_bucket_id, PUBLIC_KEY, PRIVATE_KEY)
                        
    else:
        print("Não foram encontrados snapshots.")

if __name__ == "__main__":
    main()
