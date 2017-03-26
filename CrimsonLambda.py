from __future__ import print_function
#from boto3.dynamodb.conditions import Key, Attr
import boto3

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
	
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------
	
def welcome():

	session_attributes = {}
	card_title = "Welcome"
	speech_output = "Welcome to the beginning"
	reprompt_text = "Please tell me the test to your question."
	should_end_session = False
	print('through the welcome function')
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

		
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the test skill " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    print('session ended successfully')
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def test_intent_stuff(intent, session):
	session_attributes = {}
	print('Entered the test intent')
	
	#"dynamodb.us-east-1.amazonaws.com"
	client = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='dynamodb.us-east-1.496734855354:table/8451_Transactions.amazonaws.com')
	print('set up the connection')
	#conn = boto.connect_dynamodb(aws_access_key_id='...',aws_secret_access_key='...')
	# Wait until the table exists.
	#table.meta.client.get_waiter('table_exists').wait(TableName='users')

	# Print out some data about the table.	
	#print(table.item_count)
	
	#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
	table = dynamodb.Table('8451_Transactions')
	print('Got to the table')
	#dynamodb = boto3.resource('dynamodb')
	#table = dynamodb.Table('users')
	
	
	speech_output = "The number of items in this table is " + resource.describe_table('8451_Transactions')
	print('Set up the speech output')
	reprompt_text = None
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))		

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

		  
def on_launch(launch_request, session):
	"""Called when the user launches the skill wihtout specifying what they want"""
	
	print("on_launch requestId=" + launch_request['requestId'] +
		", sessionId=" + session['sessionId'])
	#Go to skill launch_request	
	return welcome()
	

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetTest":
        return test_intent_stuff(intent, session)
	if intent_name == "AMAZON.HelpIntent":
	    return test_welcome()
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    #else:
    #    raise ValueError("Invalid intent")
	
	
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

	
	
"""
def lambda_handler(event, context):
    for record in event['Records']:
        print(record['eventID'])
        print(record['eventName'])       
    print('Successfully processed %s records.' % str(len(event['Records'])))
"""	
# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])	
	