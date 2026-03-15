#!/usr/bin/env python3

import time
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, List
import requests
import boto3
from botocore.exceptions import ClientError
import json
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ApplicationMonitor:
    def __init__(self, config_path: str = 'monitor_config.json'):
        self.config = self._load_config(config_path)
        self.check_count = 0
        self.fail_count = 0
        self.recovery_count = 0
        self.aws_clients = self._init_aws_clients()

    def _load_config(self, config_path: str) -> Dict:
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._default_config()

    def _default_config(self) -> Dict:
        return {
            "app_url": os.getenv('APP_URL', 'http://localhost:5000'),
            "health_endpoint": "/health",
            "check_interval": int(os.getenv('CHECK_INTERVAL', '60')),
            "timeout": int(os.getenv('TIMEOUT', '30')),
            "max_failures": int(os.getenv('MAX_FAILURES', '3')),
            "recovery_enabled": os.getenv('RECOVERY_ENABLED', 'true').lower() == 'true',
            "notification_enabled": os.getenv('NOTIFICATION_ENABLED', 'true').lower() == 'true',
            "slack_webhook_url": os.getenv('SLACK_WEBHOOK_URL'),
            "email_notifications": {
                "enabled": os.getenv('EMAIL_ENABLED', 'false').lower() == 'true',
                "smtp_server": os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
                "smtp_port": int(os.getenv('SMTP_PORT', '587')),
                "email_user": os.getenv('EMAIL_USER'),
                "email_password": os.getenv('EMAIL_PASSWORD'),
                "to_emails": os.getenv('TO_EMAILS', '').split(','),
                "from_email": os.getenv('FROM_EMAIL')
            },
            "aws": {
                "region": os.getenv('AWS_REGION', 'us-east-1'),
                "sns_topic_arn": os.getenv('SNS_TOPIC_ARN')
            },
            "recovery_actions": {
                "restart_container": True,
                "restart_service": True,
                "scale_up": True
            },
            "docker": {
                "container_name": os.getenv('DOCKER_CONTAINER_NAME', 'school-saas-app'),
                "service_name": os.getenv('DOCKER_SERVICE_NAME', 'school-saas')
            },
            "kubernetes": {
                "enabled": os.getenv('K8S_ENABLED', 'false').lower() == 'true',
                "namespace": os.getenv('K8S_NAMESPACE', 'school-saas'),
                "deployment_name": os.getenv('K8S_DEPLOYMENT', 'school-saas-app')
            }
        }

    def _init_aws_clients(self) -> Dict:
        clients = {}
        try:
            clients['sns'] = boto3.client('sns', region_name=self.config['aws']['region'])
            clients['cloudwatch'] = boto3.client('cloudwatch', region_name=self.config['aws']['region'])
            clients['ecs'] = boto3.client('ecs', region_name=self.config['aws']['region'])
            logger.info("AWS clients initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {e}")
        return clients

    def check_application_health(self) -> bool:
        """Check if the application is healthy"""
        url = f"{self.config['app_url']}{self.config['health_endpoint']}"
        try:
            response = requests.get(url, timeout=self.config['timeout'])
            is_healthy = response.status_code == 200
            logger.info(f"Health check: {url} - Status: {response.status_code}")
            return is_healthy
        except requests.exceptions.Timeout:
            logger.warning(f"Health check timed out: {url}")
            return False
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error during health check: {url}")
            return False
        except Exception as e:
            logger.error(f"Error during health check: {e}")
            return False

    def send_slack_notification(self, message: str, is_critical: bool = False):
        """Send notification to Slack"""
        if not self.config['notification_enabled'] or not self.config['slack_webhook_url']:
            return

        color = 'danger' if is_critical else 'good'
        webhook_url = self.config['slack_webhook_url']

        payload = {
            "attachments": [
                {
                    "color": color,
                    "text": message,
                    "footer": "Application Monitor",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Slack notification sent successfully")
            else:
                logger.error(f"Failed to send Slack notification: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")

    def send_email_notification(self, subject: str, message: str):
        """Send email notification"""
        email_config = self.config['email_notifications']
        if not email_config['enabled']:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = ', '.join(email_config['to_emails'])
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['email_user'], email_config['email_password'])
                server.send_message(msg)

            logger.info("Email notification sent successfully")
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")

    def send_sns_notification(self, message: str, subject: str):
        """Send SNS notification"""
        sns_topic_arn = self.config['aws'].get('sns_topic_arn')
        if not sns_topic_arn or 'sns' not in self.aws_clients:
            return

        try:
            self.aws_clients['sns'].publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject=subject
            )
            logger.info("SNS notification sent successfully")
        except Exception as e:
            logger.error(f"Error sending SNS notification: {e}")

    def send_notifications(self, message: str, subject: str, is_critical: bool = False):
        """Send notifications through all enabled channels"""
        logger.info(f"Sending notification: {subject}")
        self.send_slack_notification(message, is_critical)
        self.send_email_notification(subject, message)
        self.send_sns_notification(message, subject)

    def publish_cloudwatch_metric(self, metric_name: str, value: float, unit: str = 'Count'):
        """Publish metric to CloudWatch"""
        if 'cloudwatch' not in self.aws_clients:
            return

        try:
            self.aws_clients['cloudwatch'].put_metric_data(
                Namespace='SchoolSaaS/Monitoring',
                MetricData=[{
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit,
                    'Timestamp': datetime.now()
                }]
            )
        except Exception as e:
            logger.error(f"Error publishing CloudWatch metric: {e}")

    def restart_docker_container(self) -> bool:
        """Restart Docker container"""
        container_name = self.config['docker']['container_name']
        try:
            os.system(f'docker restart {container_name}')
            logger.info(f"Restarted Docker container: {container_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart Docker container: {e}")
            return False

    def restart_docker_service(self) -> bool:
        """Restart Docker service"""
        service_name = self.config['docker']['service_name']
        try:
            os.system(f'docker compose -f /opt/{service_name}/docker-compose/docker-compose.yml restart')
            logger.info(f"Restarted Docker service: {service_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart Docker service: {e}")
            return False

    def restart_kubernetes_deployment(self) -> bool:
        """Restart Kubernetes deployment"""
        if not self.config['kubernetes']['enabled']:
            return False

        namespace = self.config['kubernetes']['namespace']
        deployment_name = self.config['kubernetes']['deployment_name']

        try:
            os.system(f'kubectl rollout restart deployment/{deployment_name} -n {namespace}')
            logger.info(f"Restarted Kubernetes deployment: {deployment_name} in namespace: {namespace}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart Kubernetes deployment: {e}")
            return False

    def recover_application(self) -> bool:
        """Attempt to recover the application"""
        logger.warning("Starting recovery procedures...")
        self.recovery_count += 1

        recovery_actions = self.config['recovery_actions']

        if recovery_actions.get('restart_container'):
            if self.restart_docker_container():
                time.sleep(10)
                if self.check_application_health():
                    self.send_notifications(
                        f"Application recovered successfully by restarting container. Recovery count: {self.recovery_count}",
                        f"✅ Application Recovered - {self.config['app_url']}"
                    )
                    return True

        if recovery_actions.get('restart_service'):
            if self.restart_docker_service():
                time.sleep(15)
                if self.check_application_health():
                    self.send_notifications(
                        f"Application recovered successfully by restarting service. Recovery count: {self.recovery_count}",
                        f"✅ Application Recovered - {self.config['app_url']}"
                    )
                    return True

        if self.config['kubernetes']['enabled']:
            if self.restart_kubernetes_deployment():
                time.sleep(30)
                if self.check_application_health():
                    self.send_notifications(
                        f"Application recovered successfully by restarting Kubernetes deployment. Recovery count: {self.recovery_count}",
                        f"✅ Application Recovered - {self.config['app_url']}"
                    )
                    return True

        logger.error("All recovery attempts failed")
        self.send_notifications(
            f"❌ CRITICAL: All recovery attempts failed for {self.config['app_url']}. Manual intervention required!",
            f"🚨 Application Recovery Failed - {self.config['app_url']}",
            is_critical=True
        )
        return False

    def run(self):
        """Main monitoring loop"""
        logger.info("Starting application monitor...")
        logger.info(f"Monitoring: {self.config['app_url']}")
        logger.info(f"Check interval: {self.config['check_interval']} seconds")
        logger.info(f"Max failures before recovery: {self.config['max_failures']}")

        self.send_notifications(
            f"Application monitoring started for {self.config['app_url']}",
            f"🔍 Application Monitor Started - {self.config['app_url']}"
        )

        consecutive_failures = 0

        try:
            while True:
                self.check_count += 1

                if self.check_application_health():
                    consecutive_failures = 0
                    self.publish_cloudwatch_metric('HealthCheckStatus', 1)
                    logger.info(f"✅ Application is healthy (Check #{self.check_count})")

                    if self.fail_count > 0:
                        self.send_notifications(
                            f"Application is back to normal. Previous failures: {self.fail_count}",
                            f"✅ Application Restored - {self.config['app_url']}"
                        )
                        self.fail_count = 0

                else:
                    consecutive_failures += 1
                    self.fail_count += 1
                    self.publish_cloudwatch_metric('HealthCheckStatus', 0)
                    self.publish_cloudwatch_metric('ConsecutiveFailures', consecutive_failures)

                    logger.warning(f"❌ Health check failed (Check #{self.check_count}, Failure #{self.fail_count}, Consecutive: {consecutive_failures})")

                    if consecutive_failures >= self.config['max_failures']:
                        self.send_notifications(
                            f"Application health check failed {consecutive_failures} consecutive times. Attempting recovery...",
                            f"⚠️ Application Unhealthy - {self.config['app_url']}",
                            is_critical=True
                        )

                        if self.config['recovery_enabled']:
                            if self.recover_application():
                                consecutive_failures = 0
                                self.publish_cloudwatch_metric('RecoverySuccess', 1)
                            else:
                                self.publish_cloudwatch_metric('RecoveryFailure', 1)
                        else:
                            logger.warning("Recovery is disabled, skipping recovery attempts")

                time.sleep(self.config['check_interval'])

        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
            self.send_notifications(
                f"Application monitoring stopped. Total checks: {self.check_count}, Failures: {self.fail_count}, Recoveries: {self.recovery_count}",
                f"🛑 Application Monitor Stopped - {self.config['app_url']}"
            )
        except Exception as e:
            logger.error(f"Monitor crashed: {e}")
            self.send_notifications(
                f"Application monitor crashed: {str(e)}",
                f"🚨 Monitor Crashed - {self.config['app_url']}",
                is_critical=True
            )
            raise


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Application Health Monitor and Recovery Tool')
    parser.add_argument('--config', type=str, default='monitor_config.json',
                       help='Path to configuration file (default: monitor_config.json)')
    parser.add_argument('--test', action='store_true',
                       help='Run a single health check and exit')
    args = parser.parse_args()

    monitor = ApplicationMonitor(args.config)

    if args.test:
        is_healthy = monitor.check_application_health()
        status = "Healthy ✅" if is_healthy else "Unhealthy ❌"
        print(f"\n{monitor.config['app_url']} - {status}\n")
        sys.exit(0 if is_healthy else 1)

    monitor.run()


if __name__ == '__main__':
    main()
