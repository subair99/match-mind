from aws_cdk import RemovalPolicy, Stack
from aws_cdk import aws_dynamodb as ddb
from aws_cdk import aws_s3 as s3
from constructs import Construct


class StorageStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        s3.Bucket(self, "Footage", removal_policy=RemovalPolicy.RETAIN)
        ddb.Table(
            self,
            "EventIndex",
            partition_key=ddb.Attribute(name="match_id", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="event_id", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
        )
