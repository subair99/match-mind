"""CDK entry point. Run with: cd infra && npx cdk synth --app "uv run python app.py\""""
import aws_cdk as cdk

from matchmind_infra.stacks.storage import StorageStack

app = cdk.App()
StorageStack(app, "MatchMindStorage")
# TODO: IngestStack, ApiStack, ObservabilityStack
app.synth()
