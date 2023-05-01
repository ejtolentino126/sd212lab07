#this program calculates the predicted score of a type of assignment based on how long they took to do it.
import json
import pandas as pd
import matplotlib.pyplot as plt


def score(df):
    """This function takes a dataframe of Time, Points, Successes, and Users and turns into a df of Time, User, Score.
    Takes a dataframe as argument. Returns a list of dictionaries of time, user, score"""
    submission = {}
    SUBMISSION = []
    # gettings the max number of points
    newdf = df[["Time", "Points"]]
    max_count = newdf.groupby('Time')['Points'].sum()
    new_max = max_count.iloc[0]
    # getting the number of points 
    firstdf = (newdf.groupby(['Time']).count())
    dict_time=(firstdf.to_dict())
    times = dict_time["Points"]
    for time in times.keys():
        total = 0
        entry = df[df["Time"]==time]
        for i, row in entry.iterrows():
            if row["Success"] == 1:
                total += row["Points"]
        grade =  total / new_max * 100
        entry["score"] = grade
        # print(entry)
        firstrow = entry.iloc[:1]
        submission = firstrow[["Time", "Users", "score"]].to_dict()
        SUBMISSION.append(submission)
    return(SUBMISSION)

def turn_to_df(list):
    """this function takes the list of dictionaries from the score function and turns them into a new df"""
    NEWTIME = []
    PERSON = []
    SCORE = []
    for submission in list:
        timestamp =submission["Time"]
        for val in timestamp.values():
            NEWTIME.append(val)
        superhero = submission["Users"]
        for hero in superhero.values():
            PERSON.append(hero)
        scores = submission["score"]
        for grade in scores.values():
            SCORE.append(grade)
    assignmentdata = {"Time": NEWTIME,
                    "Person": PERSON,
                    "Score": SCORE
                    }
    assigndf = pd.DataFrame(assignmentdata)
    return(assigndf)

def clean_json(data, assignment):
    """This function goes through the large json file and gets the variables we are using: Time, Points, Success, Users.
      This accepts the json file and what assignment to look at as parameters. Returns a dataframe."""
    d = {}
    POINTS = []
    SUCCESS = []
    TIME = []
    USERS = []
    #looping over the indices in the json:
    for i in range(len(data)):
        course = data[i]["course"] #course (SD211/SD212)
        if course == "SD212":
            hw = data[i]["project"] #name of project (this takes the input from user to see what assign. to look at)
            if hw == assignment:
                user = (data[i]["user"]) 
                USERS.append(user)
                point = data[i]["points"]
                POINTS.append(point)
                if_pass = data[i]["pass"]
                SUCCESS.append(if_pass)
                time = pd.to_datetime(data[i]["datestamp"])
                TIME.append(time)
                info = {"Time":TIME, #creates a dictionary of time,points, success, and users
                        "Points": POINTS,
                        "Success": SUCCESS,
                        "Users": USERS
                        }
                newdf = pd.DataFrame(info) #turns dictionary into df
    return(newdf)

def refined_df(assigndf):
    """This takes the dataframe that has Time, Person, Score and creates a better dataframe consisting of:
    Person, Highest Score, Total Time, First and Last Submission, and Num of Submissions. Takes df as parameter. Returns a df."""
    num_submissions = (assigndf.groupby(['Person']).count()) #groups dataframe by person
    PERSON = [] #initializing lists
    SUBS = []
    HIGHEST_SCORE = [] 
    TOTAL_TIME = []
    LAST_TIME = []
    FIRST_TIME = []
    for i, row in num_submissions.iterrows(): #looking over the rows in the groupby df
        PERSON.append(i)
        SUBS.append(row["Time"]) #this is the number of submissions
        person = assigndf.loc[assigndf['Person'] == i]
        last_sub_time = (max(person["Time"]))
        LAST_TIME.append(last_sub_time)
        first_sub_time = min(person["Time"])
        FIRST_TIME.append(first_sub_time)
        total_time = last_sub_time - first_sub_time
        TOTAL_TIME.append(total_time)
        highest_score = max(person["Score"])
        HIGHEST_SCORE.append(highest_score)
        
        # print("User:", i, " ", "Number of Submissions:", row["Time"]) 
    
    refinedddata = {"Person": PERSON,
                    "Highest Score": HIGHEST_SCORE, 
                    "Total Time": TOTAL_TIME,
                    "First Submission" : FIRST_TIME,
                    "Last Submission": LAST_TIME,
                    "Number of Submissions": SUBS}
    ref_df = pd.DataFrame(refinedddata) #creating new df
    return(ref_df)

def obtaining_df():
#opening the json file
    assignment = input("What assignment? ")
    f = open("submit-data.json")
    data = json.load(f)
    df = clean_json(data, assignment)
    sub = score(df)
    assigndf = turn_to_df(sub)
    fixed_df = refined_df(assigndf)
    return(fixed_df)


if __name__ == "__main__":
    # df = obtaining_df()
    # print(df)
    f = open("submit-data.json")
    data = json.load(f)
    for i in range(1,7):
        lab = "lab0" +str(i)
        print(lab)
        df = clean_json(data, lab)
        sub = score(df)
        assigndf = turn_to_df(sub)
        fixed_df = refined_df(assigndf)
        print(fixed_df)
    