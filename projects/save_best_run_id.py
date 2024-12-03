import os 
import mlflow
import boto3


os.system('mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://mlflow-wine-quality-experiments </dev/null &>/dev/null &')
os.system('sleep 5')
mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment('wine-quality-prediction')
print(mlflow.get_tracking_uri())
client = mlflow.client.MlflowClient()
runs = client.search_runs(experiment_ids='1')
print(f'len(runs): {len(runs)}')
best_run = max(runs, key=lambda run: run.data.metrics.get('balanced_accuracy', 0))
best_run_id = best_run.info.run_id
print(f'best_run_id: {best_run_id}')
ssm_client = boto3.client('ssm')

ssm_client.put_parameter(
    Name='/project/run_id',
    Value=best_run_id,
    Type='String',
    Overwrite=True
)


# print(runs)
