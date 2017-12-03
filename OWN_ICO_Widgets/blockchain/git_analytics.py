import json
import urllib.request
from requests.auth import HTTPBasicAuth
import pandas as pd
import datetime


def authentification(company):
    url = "https://api.github.com/users/" + company
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, 'deusesx', 'karinka27')
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)


def getRepoStatistics(company):
    urlData = "https://api.github.com/users/" + company +"/repos?per_page=100"

    try:
        webURL = urllib.request.urlopen(urlData)
    except Exception:
        print("no such GitAccount")
        return -1

    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    json_repo = json.loads(data.decode(encoding))

    # count stars and forks
    stars = 0
    forks = 0
    for i in range(len(json_repo)):
        project = json_repo[i]['full_name'][len(company)+1:]
        if company in project:
            stars += json_repo[i]['stargazers_count']
            forks += json_repo[i]['forks_count']

    return stars, forks, json_repo


def getRepoTimeLine(company, json_repo):
    time = []
    if(json_repo != 0):
        for i in range(len(json_repo)):
            project = json_repo[i]['full_name'][len(company)+1:]
            if company in project:
                commitsUrl = "https://api.github.com/repos/" + company +"/" + project + "/commits"
                #print(project)
                try:
                    commitsURL = urllib.request.urlopen(commitsUrl)
                except Exception:
                    continue
                commits = commitsURL.read()
                encoding = commitsURL.info().get_content_charset('utf-8')
                commits_json = json.loads(commits.decode(encoding))
                if(len(commits_json) != 0):
                    for j in range( len(commits_json)):
                        time.append(commits_json[j]['commit']['author']['date'])
    return time


def getNormalizedTimeline(time):
    # create dataframe with timeline
    time_values = pd.DataFrame(columns = ["time", "count"])
    time_values.time = time
    time_values = time_values.fillna(1)
    time_values = time_values.groupby(["time"]).sum()
    time_values["ind"] = range(len(time_values))
    time_values["time"] = time_values.index
    time_values = time_values.set_index(['ind'])
    # delete time and group by dates
    time_values['time'] = time_values['time'].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%dT%H:%M:%SZ"))
    time_values['time'] = time_values.time.apply(lambda x: x.date())
    time_values = time_values.groupby(["time"]).sum()
    time_values = time_values.reset_index()
    return time_values


def get_git_commit_widget(company):
    authentification(company)
    # stars, forks, file
    repoStatistics = getRepoStatistics(company)
    if (repoStatistics == -1):
        return False, 0, 0, 0
    commits_json = getRepoTimeLine(company,repoStatistics[2])
    time_pd = getNormalizedTimeline(commits_json)
    x = list(time_pd['time'])
    y = list(time_pd['count'])
    return True, repoStatistics[0], repoStatistics[1], x, y
