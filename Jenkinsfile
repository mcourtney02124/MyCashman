pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                echo 'no actual building involved, just pull from GitHub  '
            }
        }
        stage ('test1') {
            steps{
                sh 'py.test test/test_sipp_utils.py'
                sh 'py.test test/test_sipp_procs.py'
                sh 'sleep 5'
            }
        }
        stage('deploy') {
            steps {
                sh './bootstrap_local.sh &'
                sh 'sleep 10'
            }
        }
        stage('test2') {
            steps {
                sh 'py.test test/test_MyCashman.tavern.yaml'
                sh 'py.test test/test_MyCashman.py'
                sh 'py.test test/test_MyCashman_shutdown.tavern.yaml'
                sh 'sleep 20'
            }
        }
    }
}