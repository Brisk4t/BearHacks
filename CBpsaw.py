import praw,re,time,requests,os,openai
import spacy
from spacy.tokens import Token
from spacy.matcher import Matcher
from pmaw import PushshiftAPI
import textblob
from textblob import TextBlob




start = time.time()

course_list = []
# for i in course_list:

# Define the course name pattern using a regular expression
pattern = [{"NORM": {"REGEX": r"CMPUT\s?\d{3}"}}]


nlp = spacy.load("en_core_web_sm")

# Create a Matcher object
matcher = Matcher(nlp.vocab)

# Add the course name pattern to the Matcher
matcher.add('COURSE_NAME', [pattern])


"""# Define the custom tokenizer function
def custom_tokenizer(doc):
    # Tokenize the text using the default tokenizer
    tokens = [token for token in doc]

    # Use the Matcher to find course names in the tokenized text
    matches = matcher(doc)
    for match_id, start, end in matches:
        # Create a new Token object to represent the course name
        course_name_token = Token(doc, start, end)
        # Set the text of the Token to the matched text
        course_name_token.text = doc[start:end].text
        # Replace the matched tokens with the course name Token
        doc[start:end] = course_name_token
    # Return the updated doc
    return doc"""

# Different Variations of a word so we can search 
def get_variations(string):
    variations = []
    variations.append(str)
    # Remove spaces
    no_spaces = string.replace(" ", "")
    variations.append(no_spaces)
    # Lowercase
    lowercase = string.lower()
    variations.append(lowercase)
    # Uppercase
    uppercase = string.upper()
    variations.append(uppercase)
    # First letter uppercase(capitalize), rest lowercase
    capitalized = string.capitalize()
    variations.append(capitalized)
    return variations




api = PushshiftAPI()
#ex_var = get_variations("CMPUT 267")
#query = ex_var[0] or ex_var[1] or ex_var[2] or ex_var[3] or ex_var[4]
#query = "(CMPUT 272 OR Cmput 272 OR cmput 272 OR CMPUT272 OR Cmput272 OR cmput272) AND (difficulty OR challenging OR hard OR tough OR demanding)"
#keywords = ["CMPUT 272", "Cmput 272", "cmput 272", "CMPUT272", "Cmput272", "cmput272"]
#difficulty_keywords = ["difficulty", "challenging", "hard", "tough", "demanding"]

comments = api.search_comments(q = "MATH 100"
,subreddit="uAlberta", size=30, sort = "desc" , sort_type =  "score" )
comment_list = []
for comment in comments: 
    if any(word in comment.get("body") for word in ["difficulty","easy","challenging", "hard" ,"hardest","difficult","worst"]):
        cmnt_body = comment.get("body")
        #print(cmnt_body)
        comment_list.append(comment)
print("**************************")


# Create empty list for the classified comments
mainly_about_course = []

# Iterate over the comments
for comment in comment_list:
    cmnt_body = comment.get("body")
    cmnt_body = cmnt_body.lower()
    cmnt_body = cmnt_body.replace("math 100","math100")
    cmnt_sentance = cmnt_body.split(".")
    #print("CMMNT",cmnt_sentance)
    main_cmmnt = 'none'
    for i in cmnt_sentance:
        if ("math100" in i):
            for z in ["difficulty","easy","challenging", "hard" ,"demanding","difficult","worst"]  :
                if (z in i):
                    main_cmmnt = i
                    #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",main_cmmnt)
                    break
        else: 
            cmnt_sentance.remove(i)
    if main_cmmnt == 'none' :
        continue
    # Tokenize consediring dependencies 
    doc = nlp(main_cmmnt)
    #doc = custom_tokenizer(doc)

    # Initialize a flag to track whether the comment is mainly about CMPUT 272
    is_mainly_about_cmput_272 = False
    
    # Check if the main subject of the comment is CMPUT 272
    for token in doc:
        #print("dependencies:",token.dep_)
        if token.dep_ == "nsubj"  and token.text.lower() == "math100":
            is_mainly_about_cmput_272 = True
            break
    
    # If the main subject is CMPUT 272, add the comment to the mainly_about_cmput_272 list
    if is_mainly_about_cmput_272:       
        mainly_about_course.append(main_cmmnt)

print(":::::::::::::WANTED COMMENTS :::::::::::::::::")
for i in mainly_about_course:

    print("-------------------------------------------------")
    print(i)
    print("-------------------------------------------------")

end = time.time()
elapsed_time = end - start

# Print the elapsed time
print("Elapsed time: ", elapsed_time)

# sentiment analysis by textblob
def classify_sentiment(comment):
    analysis = TextBlob(comment)
    #TextBlob.word_sentiment_associations.update({"hard": -1})
    score = analysis.sentiment.polarity
    return score

# Iterate over the list of comments and classify the sentiment of each one
sentiment_avg = 0
sentiment_num = 0
for comment in mainly_about_course:
    sentiment_num += 1
    sentiment = classify_sentiment(comment)
    sentiment_avg +=  sentiment
    print(f'Comment: {comment} -- Sentiment Score: {sentiment}')

print ( " TEXTBLOB COURSE FINAL SENTIMENT: ",sentiment_avg/sentiment_num)


"""#sentiment analysis by GPT
def gpt_sentiment(txtex):

    openai.api_key = "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"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= f"perform sentiment analysis on the following and give score form -1 to 1, where -1 is very negative and 1 is very positve. Just give a number.: {txtex}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response

sentiment_avg = 0
sentiment_num = 0
for comment in mainly_about_course:
    sentiment_num += 1
    sentiment = gpt_sentiment(comment)
    num_unstrip = (sentiment['choices'][0]['text'])
    num = "".join(num_unstrip.splitlines())
    num = float(num)
    sentiment_avg +=  num
    print(f'Comment: {comment} -- Sentiment Score: {num}')

print ( " GPT COURSE FINAL SENTIMENT: ",sentiment_avg/sentiment_num)"""