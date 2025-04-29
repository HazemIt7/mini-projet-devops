// Définition du pipeline déclaratif
pipeline {
    // Agent : Où exécuter le pipeline. 'any' signifie n'importe quel agent disponible.
    agent any

    // Variables d'environnement globales pour le pipeline
    environment {
        // Nom de l'image Docker (utilisez votre nom d'utilisateur Docker Hub si vous poussez l'image)
        DOCKER_IMAGE_NAME = 'hazem911/mini-projet-devops'
        // Ou sans push vers Docker Hub:
        // DOCKER_IMAGE_NAME = 'mon-app-web-jenkins'
        DOCKER_IMAGE_TAG = "latest" // Vous pouvez aussi utiliser le numéro de build: ${BUILD_NUMBER}
        CONTAINER_NAME = 'webapp-jenkins' // Nom du conteneur qui sera lancé
    }

    // Les étapes (stages) du pipeline
    stages {
        // Étape 1: Récupérer le code source depuis Git
        stage('Checkout') {
            steps {
                // Commande pour cloner/récupérer le code
                git url: 'https://github.com/HazemIt7/mini-projet-devops.git', branch: 'main' // Remplacez par l'URL de VOTRE repo et la bonne branche !
            }
        }
        
        // Étape de linting pour vérifier le code Python
        stage('Lint') {
            steps {
                script {
                    // Conteneur Python temporaire
                    docker.image('python:3.9-slim').inside {
                        sh 'pip install --no-cache-dir flake8'
                        sh 'flake8 .'
                    }
                }
            }
        } 

        // étape de test: Utiliser un conteneur Python temporaire pour isoler les tests
        stage('Test') {
            steps {
                script {

                    
                    docker.image('python:3.9-slim').inside {
                        sh 'pip install --no-cache-dir -r requirements.txt'
                        sh 'pytest -v' // -v pour plus de détails
                    }
                    
                }
            }
        }
        // test docker
        stage('Test Docker') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }
        // Étape 2: Construire l'image Docker
        stage('Build Docker Image') {
            steps {
                script {
                    // Utilise les fonctions du plugin Docker Pipeline
                    // Construit l'image avec le nom et le tag définis plus haut
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}", ".")
                }
            }
        }
        stage('Scan Image') {
            steps {
                // Exécute Trivy en tant que conteneur pour scanner l'image locale construite
                // Le montage du socket Docker permet à Trivy d'accéder aux images sur l'hôte
                // --rm supprime le conteneur Trivy après exécution
                // --exit-code 1 : Fait échouer le scan (et donc le build) si des vulnérabilités HIGH ou CRITICAL sont trouvées
                // --severity HIGH,CRITICAL : Ne rapporte que ces niveaux de sévérité
                sh """
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                """
                // Pour juste afficher le rapport sans faire échouer le build, enlevez --exit-code 1
                // Pour voir toutes les vulnérabilités, enlevez --severity HIGH,CRITICAL
            }
        }

        // Étape 3: (Optionnel) Pousser l'image sur Docker Hub
        // Décommentez ce stage si vous avez configuré les credentials Docker Hub
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Utilise les credentials configurés dans Jenkins (ID: 'dockerhub-credentials')
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        // Pousse l'image vers Docker Hub
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                    }
                }
            }
        }
        

        // Étape 4: Déployer/Lancer le conteneur
        stage('Run Container') {
            steps {
                // Utilise des commandes shell pour gérer le conteneur
                sh """
                # Arrêter et supprimer un conteneur existant avec le même nom (s'il existe)
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true

                # Lancer un nouveau conteneur avec la nouvelle image
                docker run -d -p 5001:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                # Note: J'utilise le port 5001 sur l'hôte pour éviter un conflit avec le port 5000 si vous l'utilisez déjà localement.
                """
            }
        }
    }

    // Actions à exécuter à la fin du build (succès, échec, etc.)
    post {
        always {
            // Toujours nettoyer l'espace de travail Jenkins
            cleanWs()
        }
        success {
            echo 'Pipeline terminé avec succès !'
        }
        failure {
            echo 'Le Pipeline a échoué.'
        }
    }
}