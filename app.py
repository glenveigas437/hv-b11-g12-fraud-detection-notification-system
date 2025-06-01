from flask import Flask, jsonify, render_template, request
import boto3
import json

app = Flask(__name__)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id='your-access-id',
    aws_secret_access_key='your-access-key',
    region_name='us-west-2'
)

@app.route('/trigger')
def trigger_lambda():
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-2:975050024946:function:FraudDetectionProjectB11G12',
        InvocationType='RequestResponse',
        Payload=b'{}'
    )

    result = response['Payload'].read().decode('utf-8')
    return jsonify({"message": "Lambda triggered", "response": result})

@app.route('/submit', methods=['POST'])
def submit_transaction():
    amount = request.form.get('amount', type=float)
    
    payload = {"amount": amount}
    
    response = lambda_client.invoke(
        FunctionName='your-function-name',  # Replace with your function name
        InvocationType='RequestResponse',
        Payload=json.dumps(payload).encode()
    )

    result = json.loads(response['Payload'].read().decode('utf-8'))
    status = json.loads(result['body'])  # Get "Fraud" or "Success"
    
    return jsonify({"message": "Lambda triggered", "response": result})
if __name__ == '__main__':
    app.run(debug=True)
