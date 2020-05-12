import boto3
import logging

from cm_util import  Constants, StageName

FORMAT = (
    "[%(levelname)s] %(asctime)-s %(funcName)s "
    "%(pathname)s:%(lineno)s => %(message)s"
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# log_handler = logger.handlers[0]
# log_handler.setFormatter(logging.Formatter(FORMAT))

dynamodb = boto3.resource("dynamodb")

stage = StageName()
STAGE = stage.get_stage_name()

consolidated_movement_transaction_table = dynamodb.Table(
    Constants.CM_TRANSACTION_TABLE.value
)


class ReconProcess():

    def get_records(self):
        transaction_scan = consolidated_movement_transaction_table.scan(
            TableName=Constants.CM_TRANSACTION_TABLE.value
        )
        return transaction_scan["Items"]

    def batch_write(self):
        with consolidated_movement_transaction_table.batch_writer() as batch:
            for r in self.get_records():
                batch.put_item(Item=r)
        logger.info("Inserted all records once agin")

ReconProcess().batch_write()