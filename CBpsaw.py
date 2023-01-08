import praw,re
import spacy
from spacy.tokens import Token
from spacy.matcher import Matcher
from pmaw import PushshiftAPI

# Define the course name pattern using a regular expression
pattern = [{"NORM": {"REGEX": r"CMPUT\s?\d{3}"}}]


nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner"])

# Create a Matcher object
matcher = Matcher(nlp.vocab)

# Add the course name pattern to the Matcher
matcher.add('COURSE_NAME', [pattern])


# Define the custom tokenizer function
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
    return doc

# Create a custom spaCy model using the custom tokenizer
nlp.tokenizer = custom_tokenizer


api = PushshiftAPI()
#query = "(CMPUT 272 OR Cmput 272 OR cmput 272 OR CMPUT272 OR Cmput272 OR cmput272) AND (difficulty OR challenging OR hard OR tough OR demanding)"
#keywords = ["CMPUT 272", "Cmput 272", "cmput 272", "CMPUT272", "Cmput272", "cmput272"]
#difficulty_keywords = ["difficulty", "challenging", "hard", "tough", "demanding"]
comments = api.search_comments(q = ("CMPUT 272" or "Cmput 272" or"cmput 272"or"CMPUT272" or "Cmput272" or "cmput272")#and("difficulty"or "challenging"or "hard" or"tough" or"demanding") ,
,subreddit="uAlberta", limit=100, sort = "desc" , sort_type =  "score" )
comment_list = []
for comment in comments: 
    if any(word in comment.get("body") for word in ["difficulty", "challenging", "hard" ,"demanding","difficult","worst"]):
        cmnt_body = comment.get("body")
        print("TST TO ADD PASSED")
        print(cmnt_body)
        comment_list.append(comment)
print("**************************")


# Load the English model for spaCy
# Create empty lists for the classified comments
mainly_about_cmput_272 = []
not_mainly_about_cmput_272 = []

# Iterate over the comments
for comment in comment_list:
    # Parse the comment using the spaCy model
    cmnt_body = comment.get("body")
    doc = nlp(cmnt_body)
    
    # Initialize a flag to track whether the comment is mainly about CMPUT 272
    is_mainly_about_cmput_272 = False
    
    # Check if the main subject of the comment is CMPUT 272
    for token in doc:
        if token.dep_ == "nsubj" and token.text.lower() == "cmput 272":
            is_mainly_about_cmput_272 = True
            break
    
    # If the main subject is CMPUT 272, add the comment to the mainly_about_cmput_272 list
    if is_mainly_about_cmput_272:
        mainly_about_cmput_272.append(comment)

print("START")
for i in mainly_about_cmput_272:
    print(i)
    print("END")