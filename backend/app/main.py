import boto3

# Initialize the Bedrock client
client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

async def get_rag_response(query: str):
    response = client.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'YOUR_KB_ID',
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-v2:0'
            }
        }
    )
    return response['output']['text']
