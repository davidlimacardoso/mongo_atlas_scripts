import requests
from requests.auth import HTTPDigestAuth

PUBLIC_KEY = "XXXXXXXXXXXX"
PRIVATE_KEY = "XXXXXXXXXXXX"
PROJECT_ID = "60bee66bf642asdqaawdasd"
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


def get_tasks_export(public_key, private_key, project_id, cluster_name):
    """
    Obtém a lista de tarefas de exportação para um determinado cluster.
    """
    url = f"{BASE_URL}/groups/{project_id}/clusters/{cluster_name}/backup/exports"
    headers = {"Accept": "application/vnd.atlas.2025-03-12+json"}
    response = requests.get(url, headers=headers, auth=HTTPDigestAuth(public_key, private_key))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter tarefas de exportação: {response.status_code} - {response.text}")
        return None

def main():
    # Obtém a lista de projetos e clusters
    project_clusters = get_projects_and_clusters(PUBLIC_KEY, PRIVATE_KEY)

    for project in project_clusters:
        if 'clusters' in project:
            print(f"Projeto: {project['name']}, ID: {project['id']}")
            for cluster in project['clusters']:
                print(f"  Cluster: {cluster}")

                # Obtém as tarefas de exportação para o cluster
                tasks = get_tasks_export(PUBLIC_KEY, PRIVATE_KEY, project['id'], cluster)
                if tasks:
                    for task in tasks["results"]:
                        print(f"Tarefa de exportação: {task['id']}")
                        print('Status da Exportação: ', task['exportStatus'])
                        print(f"Status: {task['state']}")
                        print("")
                print("*" * 50)

    else:
        print("Não foram encontrados snapshots.")

if __name__ == "__main__":
    main()
