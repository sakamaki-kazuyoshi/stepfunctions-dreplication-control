import os
import boto3
import logging

sfn_client = boto3.client('stepfunctions')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    sfn_arn=event["StateMachineId"]                 #呼び出し元ステートマシンARN（SAM側でステートマシンのARNを設定すると循環参照となる）
    sfn_current_exec_name=event["ExecutionName"]    #呼び出し元ステートマシンの実行名取得
    # イベントデータロギング
    logger.info('EventData : ' + str(event))

    # 実行中のステートマシン取得
    response = sfn_client.list_executions(
        stateMachineArn=sfn_arn,
        statusFilter='RUNNING', #実行中のステートマシンでフィルタ（一致する実行を取得）
    )

    # 実行中のステートマシンフラグ
    running_flg=False

    # 実行中のステートマシンがあるかチェック
    for sfn_exec_name in response['executions']:
      # 呼び出し元ステートマシンの実行名ロギング
      logger.info('Execution name of the running Statemachine : ' + sfn_exec_name['name'])

      # 呼び出し元以外の実行があるかどうか
      if sfn_current_exec_name != sfn_exec_name['name'] :
        running_flg=True
        logger.error('There is a running state machine')

    return {
        "running_flg": running_flg
    }