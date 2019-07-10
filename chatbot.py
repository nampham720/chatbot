
# coding: utf-8

# In[1]:


# First declaration
# Run only once to not lose information 


from nltk.corpus import wordnet, stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import re
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer




#global var
approval = ['y', 'yes', 'ok', 'approved', 'sure']
denial = ['n', 'no', 'nah', 'denied', 'nope', 'never', 'perhaps', 'maybe']
stops = set(stopwords.words('english'))
domains = {'com', 'fi', 'no', 'ai', 'ml', 'org', 'dk', 'vn'}
locations = {'finland': {'oulu', 'tampere', 'turku', 'helsinki'},
           'sweden': {'stockholm', 'gotenburg', 'malmo', 'oulu'},
           'denmark': {'copenhagen', 'odense'}}

datetime = datetime.datetime.now()


# In[2]:


########## FUNCTIONS ###############


# In[3]:


analyser = SentimentIntensityAnalyzer()

def sentiment_score(sentence):
    score = analyser.polarity_scores(sentence)
    return score['compound']


# In[4]:


def confirm_answer(answer):
    '''
    Double check if the answer is per user's purpose
    '''
    
    logic = True
    answer = answer.lower().strip()
    tracking = list()
    
    while logic:
        
        # user chooses yes ==> break the loop, return response = yes
        if answer in approval or sentiment_score(answer)>=0.05:
            logic = False
            tracking.append('y')
            return tracking[-1]
    
        # users chooses no ==> make sure the answer is no
        if answer in denial or sentiment_score(answer)<=-0.05:
            
            print("Have you selected 'No'? [y/n]")
            tracking.append(answer) #tracking the current response
            
            answer = input().lower() 
            
            # if new_answer = yes, current tracking = no ==> break the loop, final answer = no
            if answer in approval or sentiment_score(answer)>=0.05:
                logic = False
                return 'n'
            
            # new_answer = no, ask for another answer
            if answer in denial or sentiment_score(answer)<=-0.05:
                print("Please kindly re-enter your selection [y/n].")
                answer = input().lower()    

        # check if the input is valid
        if answer not in approval and answer not in denial:
            print("I don't get it. Please kindly re-enter your selection [y/n].")
            answer = input().lower()    


# In[5]:


def opening():
    
    '''
    Ask for permission
    '''
    
    print("May I ask for your company's name? [y/n]")
    answer = confirm_answer(input().lower())
    logic = True
    
    while logic:
        
        if answer not in denial and answer not in approval:
            print("Please re-select your answer: [y/n]")
            answer = confirm_answer(input().lower())
            
        
        if answer in denial or answer in approval or answer in exit:
            
            if answer.lower() == 'exit':
                print("Are you sure you want to stop the conversation? [y/n]")
                answer = confirm_answer(input().lower())
                if answer in approval:
                    print("We are very sorry to know this. Wish you a good day!")
                    break
            
            # agree to provide the company's name
            if answer in approval:
                print("Great. Let's get started!") 
                print("Be noticed that you can edit your information later on.")
                print("Most of the sections will be mandatory, would you like to continue? [y/n]")

                answer = confirm_answer(input().lower())
                
                if answer in approval:

                    print("Perfect! May we have your company's name?")
                    name = input()
                    logic = False
                    return 'approved', name
                
                if answer.lower() == 'exit':
                    print("Are you sure you want to stop the conversation? [y/n]")
                    answer = confirm_answer(input().lower())
                    if answer in approval:
                        print("We are very sorry to know this. Wish you a good day!")
                        break

            # not agree to provide info
            if answer in denial:
                print("Too sad. We just want to do the best to you. Are you sure you want to decline our support? :( [y/n]")
                answer = input().lower()
                
                # answer = no => agree to provide info
                if answer in denial:
                    print("Great. Let's get started!") 
                    print("Be noticed that you can edit your information later on.")
                    print("Most of the sections will be mandatory, would you like to continue? [y/n]")
                    answer = confirm_answer(input().lower())
                    
                    if answer in approval:
                        print("Perfect! May we have your company's name?")
                        name = input()
                        logic = False
                        return 'approved', name
                    
                
                else:
                    print("See you next time :)")
                    logic = False
                    return 'denied', logic
                


# In[6]:


def name_extract(company):
    '''
    Extract the name of the company
    '''
    # first run to extract meaning tokens and is alphabetic
    sample = [wtoken for wtoken in word_tokenize(company) if wtoken not in stops and wtoken.isalpha()]
    name = []
    
    # input = e.g: jpmorgan, hellokitty, etc.
    if len(sample) == 1:
        name.append(sample[0])
        
    else:
        for token in sample:
            # find non-sense tokens = not having any synsets
            if len(wordnet.synsets(token)) < 1:
                name.append(token)
        
    # if input is a character, by accident
    if len(sample) == 0 or len(name) == 0:
        print("Unfortunately we haven't received your answer. Please re-enter your answer:")
        name.append(input())
    
    print('=> Name is: "{}"'.format(name[0]))
    print("=> Is this correct? [y/n]")
    answer = input()
    
    response = confirm_answer(answer)
    
    if response == 'y':
        print('=> "{}". Got it!'.format(name[0]))
        return name[0]
    if response == 'n':
        print("Please write down ONLY the company's name:")
        company = input()
        name.append(company)
        print('=> "{}". Got it!'.format(name[-1]))
        return name[-1]
        
        


# In[7]:


def founded_date(founded_input):
    founded_input = re.sub("[^0-9a-zA-Z]", " ", founded_input).split()
    logic = True
    
    while True:
        
        # Check if values are accordingly prompted
        try:
            if int(founded_input[0]) and int(founded_input[1]):
                pass
        except Exception as e:
            print("=> Error!! Please follow the form: mm/yyyy")
            founded_input = input()
            founded_input = re.sub("[^0-9a-zA-Z]", " ", founded_input).split()
            
        
        # wrong input
        if len(founded_input) != 2:
            print("Please follow the form: mm/yyyy")
            founded_input = input()
            founded_input = re.sub("[^0-9a-zA-Z]", " ", founded_input).split()
            
            
        # correct input    
        if len(founded_input) == 2:
            month, year = founded_input[0], founded_input[1]
            
            #Check if lenth of month and year follow the form
            if len(founded_input[0]) in range(1, 3) and len(founded_input[1]) == 4:
                
                #Check if month is a valid value
                if not int(month) in range(1, 13):
                        print("The values are invalid. Please follow the form: mm/yyyy")
                        founded_input = input()
                        founded_input = re.sub("[^0-9a-zA-Z]", " ", founded_input).split()
                        month, year = founded_input[0], founded_input[1]

                print('=> "{}/{}" is the founded date, correct? [y/n]'.format(month, year))
                answer = input()
                response = confirm_answer(answer)
            
                if response == 'y':
                    return '{}/{}'.format(month, year)
            
                if response == 'n':
                    print("Please re-enter the information as: mm/yyyy")
                    founded_input = input()
                    founded_input = re.sub("[^0-9a-zA-Z]", " ", founded_input).split()
            
            else:
                print("The values are invalid. Please re-enter more accurate values (mm/yyyy):")
                founded_input = input()
                founded_input = re.sub("[^0-9a-zA-Z]", " ", founded_input).split()
                month, year = founded_input[0], founded_input[1]
            


# In[8]:


def email_symbol(email):
    while '@' not in email:
        print("Your email is invalid. Kindly re-enter your email address.")
        email = input().strip()
    
    endings = email.split('@')[-1] # get the part after @    
    
    while len(endings.split('.')) < 2:
        print("Your email is invalid. Kindly re-enter your email address.")
        email = input().strip()
        endings = email.split('@')[-1] # get the part after @   

    return email, endings

def valid_email(mail):
    '''
    check if an email is valid
    '''
    
    logic = True
    email, endings = email_symbol(mail)
    
    while logic:
        
        if '.' in endings:

            endings = endings.split('.') # get the part after @    
            others, domain = endings[:-1][0], endings[-1] # get the final domain
            mail_name = email.split('@')[0] # the part before @
            
        if domain == '' and others == '' and mail_name == '':
            print("Your email is invalid. Please kindly re-enter your email address.")
            email, endings = email_symbol(input().strip().lower())

        if domain != '' and others != '' and mail_name != '': 
            print("Are your sure this is your email address? [y/n]")
            answer = input().lower()
            response = confirm_answer(answer)

            #sure this is the address
            if response == 'y':
                logic = False
                return email
                domains.add(domain)
        
            if response == 'n':
                print("Please kindly re-enter your email address:")
                email, endings = email_symbol(input().lower().strip())
        
        else:
            print("Your email is invalid. Kindly re-enter your email address.")
            email, endings = email_symbol(input().lower().strip())

    
                    


# In[9]:



def contact_info(founder, mail):
    
    '''
    Double check if the information is input as wanted
    '''
    
    logic = True
    answers = ['name', 'n', 'nam', 'nae', 'ame',  
               'email', 'e', 'em', 'ail', 'mail',
              'both', 'b', 'bot', 'oth', 'boh']
    
    email = valid_email(mail)
    
    while logic:
        print('Name: {} -  Email: {}\nIs this correct? [y/n]'.format(founder, email))
        answer = input().lower()
        #if answer.lower() in denial:
        #    double_check = confirm(answer)
        
        if answer in approval:
            print("Welcome {}.".format(founder))
            logic = False
            if founder == '':
                founder = 'None'
            return founder, email
        
        if answer in denial:
            print("Which information do you want to change, Name(n) or Email(e) or both (b)?")
            answer = input().lower()
            
            if answer not in answers:
                print('Please select either "n" (name) or "e" (email) or "b" (both).')
                answer = input().lower()
            
            else:
                #name
                if answer in answers[:4]:
                    print("Please enter your name:")
                    founder = input()
                    
                #email
                if answer in answers[5:9]:
                    print("Please enter your email:")
                    email = valid_email(input())
                    
                #both
                if answer in answers[10:]:
                    print("Please enter your new contact information:")
                    print("Name:")
                    founder = input()
                    print("Email:")
                    email = valid_email(input())


# In[10]:


def description(describe):
    '''
    Check whether description is empty on purpose
    '''
    
    
    while len(describe) == 0:
        print("It seems like you have forgotten to type in your description. Would you like to try again? [y/n]")
        answer = input().lower()
        response = confirm_answer(answer)
        
        if response == 'y':
            print("Please type in your description :) :")
            describe = input()
            
        if response == 'n':
            print("Are you sure you want to skip this part? [y/n]")
            answer = input().lower()
            response = confirm_answer(answer)
            
            if response == 'y':
                print("Sure, we will skip this part.")
                return None
            
            if response == 'n':
                print("Sure. Please type in your description here:")
                describe = input()
    
    return describe


# In[11]:


def search_country(city):
    '''
    Return only the first match to reduce interacting time between customers and machines
    '''
    for country, cities in locations.items():
        if city in cities:
            return country

def update_location(city, country):
    '''
    Update the list of countries
    '''
    
    # also search for basic abbreviation: fin = finland, swe = sweden, etc.
    for location in locations.keys():
        if country in location:
            
            country = location
            cities = locations.get(country, None)
            # no cities in that country
            if city in cities:
                pass
            else:
                return cities.add(city)

        else:
            locations.update({country: set()})
            cities = locations.get(country)
            return cities.add(city)

    
def location_fb(city):
    '''
    Location feedback: double check with user wheher to update the location
    '''
    
    country = search_country(city.lower())
    
    while country == None:
        print("Ops! We can't locate where you are. Would you please tell us in which country it is?")
        country = input()
        
    while len(country) == 0:
        print("Seems like you have forgotten to type in the answer. Please kindly re-enter your answer.")
        country = input()
    
    logic = True
    while logic:
        print("{} in {}?[y/n]".format(city.upper(), country.upper()))
        answer = input().lower()
        answer = confirm_answer(answer)
    
        if answer == 'y':
            print('Cool! We got it now!')
            update_location(city.lower(), country.lower())
            logic = False
            return city, country
        
        if answer == 'n':
            print("Would you please tell us in which country it is?")
            country = input()
            print("=> {} in {}? [y/n]".format(city.upper(), country.upper()))
            answer = input().lower()
            answer = confirm_answer(answer)

            if answer == 'y':
                print("Cool! We will update our database now.")
                update_location(city.lower(), country.lower())
                logic = False
                return city, country


# In[12]:


def edit(answer):
    '''
    Edit answers
    '''
    
    options = ['c', 'e', 'p', 'd', 'n', 'l']
    
    while answer not in options:
        print("Please re-select your answer:")
    

        print("'c' for Company")
        print("'e' for Established Date")
        print("'p' for Contact Information")
        print("'d' for Description")
        print("'n' for None")
        
        answer = input().lower()
        
    if answer == 'c':
        print("Please enter ONLY your company's name again:")
        
        company = input()
        company = name_extract(company)
        return answer, company
        
    if answer == 'e':
        print("Please enter your established date again (mm/yyy):")
        founded_input = input()
        founded_input = founded_date(founded_input)
        return answer, founded_input
    
    if answer == 'p':
        print("Please enter the founder's name again:")
        name = input()
        print("Please enter the email address again:")
        email = input()
        return answer, contact_info(name, email)
    
    if answer == 'd':
        print("Please enter the description again:")
        describe = input()
        describe = description(describe)
        return answer, describe
    
    if answer == 'l':
        print("Please enter the city again:")
        city = input().lower()
        city, country = location_fb(city)
    
    if answer == 'n':
        return answer, _


# In[13]:


# Create a dataframe to keep track with data and for fur furtherwork
# Either to export as a csv file 
# Or to use as temporary database
# It can be pushed to cloud later

global df
df = pd.DataFrame({'Consent': [],
                  'Company': [],
                  'Founder': [],
                   'Email': [],
                   'Founded': [],
                  'Description': [],
                   'City': [],
                   'Country': [],
                  'Time': []})

def add_data(func):
    def inner(data):
        returned_value = func(data)
        return returned_value
    return inner

@add_data
def data_to_add(result):

    
    df.loc[-1] = result
    df.index = df.index + 1
    #df = df.sort_index()
    return df


# In[14]:


########### MAIN ##########


# In[15]:


try:
    answer, company = opening()
except Exception as e:
    print("\nUser stops the conversation.")

    
if answer in approval:
    company = name_extract(company)
    
    print("May we please ask for your name and email address?")
    print("Name:")
    founder = input()
    print("Email address:")
    email = input()
    founder, email = contact_info(founder, email)
    
    print("What about the established date? When was your company founded? Please follow the form: mm/yyyy")
    founded_input = input()
    founded_input = founded_date(founded_input)
    
    print("You may want to tell us a little bit about your company, may you not?")
    describe = input()
    describe = description(describe)
    
    print("Final information. May you please tell us your location (city)?")
    city = input()
    city, country = location_fb(city.lower())
    
    print("\nHere is information you have given:\n")
    print('Company: {}\nEstablished date: {}\nFounder: {}\nEmail address: {}\nDescription: {}\nCity: {}\nCountry: {}'.format(company, founded_input, founder, email, describe, city, country))
    
    
    print("\nIs there any section that you would like to edit?")
    
    print("Please select:")
    print("'c' for Company")
    print("'e' for Established Date")
    print("'p' for Contact Information")
    print("'d' for Description")
    print("'l' for Location")
    print("'n' for None")
    answer = input().lower()
    
    logic = True
    while logic:
        
        if answer == 'n':
            logic = False
            print("Thank you for your participation!")
            print("\nShould there is any change you'd like to make, do not hesitate to contact us at")
            print("\tEmail address: abc@valuer.ai\n\tTelephone: +12345678")
            print("Goodbye and have a nice day!")


            result = ["agreed", company, founder, email, founded_input, describe, city, country, datetime]
            break
    
    
        if answer != 'n':
            if answer == 'p':
                _, response = edit(answer)
                founder, email = response[0], resposne[1]
                
                print("\nHere is information you have given:\n")
                print('Company: {}\nEstablished date: {}\nFounder: {}\nEmail address: {}\nDescription: {}\nCity: {}\nCountry: {}'.format(company, founded_input, founder, email, describe, city, country))
    
                result = ["agreed", company, founder, email, founded_input, describe, city, country, datetime]
            
            if answer == 'l':
                _, response = edit(answer)
                city, country = response[0], response[1]
                
                

            else:
                option, response = edit(answer)
                if option == 'c':
                    company = response
                if option == 'e':
                    founded_input = response
                if option == 'd':
                    describe = response

                result = ["agreed", company, founder, email, founded_input, describe, city, country, datetime]

                
                print("\nHere is information you have given:\n")
                print('Company: {}\nEstablished date: {}\nFounder: {}\nEmail address: {}\nDescription: {}\nCity: {}\nCountry: {}'.format(company, founded_input, founder, email, describe, city, country))
        
        print("\nIs there anything you want to change?[y/n]")
        rep = input().lower()
        rep = confirm_answer(rep)
        
        if rep =='y':
            print("Please select:")
            print("'c' for Company")
            print("'e' for Established Date")
            print("'p' for Contact Information")
            print("'d' for Description")
            print("'n' for None")
            answer = input().lower()
            
        if rep == 'n':
            print("Thank you for your participation!")
            print("\nShould there is any change you'd like to make, do not hesitate to contact us at")
            print("\tEmail address: abc@xyz.ai\n\tTelephone: +12345678")
            print("Goodbye and have a nice day!")
            
            logic = False
            break
            
    try:
        data_to_add(result)   
    except Exception as e:
        print("User did not finish the conversation.")


# In[16]:


df


# In[17]:


domains

