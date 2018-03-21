pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'no actual building involved, just pull from GitHub  '
            }
        }
        stage('deploy') {
            steps {
                sh './bootstrap_local.sh &'
                sh 'sleep 10'
            }
        }
        stage('test') {
            steps {
                sh 'py.test test/test_MyCashman.tavern.yaml'
                sh 'py.test test/test_MyCashman.py'
                sh 'py.test test/test_MyCashman_shutdown.tavern.yaml
                sh 'sleep 20'
            }
        }
    }
}