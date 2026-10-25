pipeline {
    agent any

    environment {
        PLAYWRIGHT_BROWSERS_PATH = "${WORKSPACE}\\pw-browsers"
    }

    stages {
        stage('Setup') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt --default-timeout=300 --retries 10'
                bat 'venv\\Scripts\\python -m playwright install chromium'
            }
        }

        stage('Start Website') {
            steps {
                bat 'start "" /B venv\\Scripts\\python -m http.server 8000'
                bat 'ping -n 4 127.0.0.1 >nul'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'venv\\Scripts\\python -m pytest --junitxml=results.xml --html=report.html --self-contained-html'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'results.xml'
            archiveArtifacts artifacts: 'report.html, test-results/**', allowEmptyArchive: true
        }
        success { echo 'Saare tests pass hue' }
        failure { echo 'Kuch tests fail hue' }
    }
}
