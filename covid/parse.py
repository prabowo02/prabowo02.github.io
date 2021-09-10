# Data from https://covid.ourworldindata.org/data/owid-covid-data.csv

import csv
import datetime
import json
import os


MANUAL_FIX_DATA = {
    'IDN': {
        '2021-09-02': 680,
        '2021-09-03': 574,
    }
}

USER_PROFILE = {
    'IDN': {
        'region': 'Indonesia',
        'flag': 'ID',
        'rank': 'President',
        'birth': 1961,
        'covid_status': 'new_deaths',
        'contest_name': 'Indonesia New COVID-19 Deaths',
        'username': 'jokowi',
        'wins': 2,
        'affiliation': 'Istana Negara',
        'current_rank': '1 Dan',
        'to_promote': '131',
    },
    'SGP': {
        'region': 'Singapore',
        'flag': 'SG',
        'rank': 'Prime Minister',
        'birth': 1952,
        'covid_status': 'new_cases',
        'contest_name': 'Singapore New COVID-19 Cases',
        'username': 'leehsienloong',
        'wins': 5,
        'affiliation': 'The Istana',
        'current_rank': '3 Kyu',
        'to_promote': '174',
    }
}

RATING_COLOR = ((0, 'gray'), (400, 'brown'), (800, 'green'), (1200, 'cyan'), (1600, 'blue'), (2000, 'yellow'), (2400, 'orange'), (2800, 'red'))

def get_rating_color(rating):
    res = None
    for bound, color in RATING_COLOR:
        if rating >= bound:
            res = color
    return res


def get_rating_history(country, covid_status, contest_name):
    rating_history = []
    old_rating = 0
    manual_fix_data = MANUAL_FIX_DATA.get(country, {})
    with open('owid-covid-data.csv') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if row['iso_code'] != country:
                continue

            new_rating = row[covid_status].replace(',', '')
            if not new_rating:
                continue
            new_rating = int(float(new_rating))

            if row['date'] in manual_fix_data:
                new_rating = manual_fix_data[row['date']]

            rating_history.append({
                'ContestName': contest_name,
                'OldRating': old_rating,
                'NewRating': new_rating,
                'EndTime': int(datetime.datetime.timestamp(datetime.datetime.strptime(row['date'], '%Y-%m-%d'))),
                'Place': 1,
                'StandingsUrl': '#',
            })
            old_rating = new_rating

    return rating_history


def get_rating_stats(rating_history):
    return {
        'CurrentRating': rating_history[-1]['NewRating'],
        'HighestRating': max(rating['NewRating'] for rating in rating_history),
        'RatedMatches': len(rating_history),
        'LastCompeted': datetime.datetime.fromtimestamp(rating_history[-1]['EndTime']).strftime('%Y/%m/%d'),
    }


def get_html(country):
    # These still need to be manually modified: current rating color, highest rating color, rank, delta needed to promote
    profile = USER_PROFILE[country]
    rating_history = get_rating_history(country, profile['covid_status'], profile['contest_name'])
    rating_stats = get_rating_stats(rating_history)
    return f'''<html>
  <head>
    <title>COVID-19</title>
    <link href="https://fonts.googleapis.com/css?family=Lato:400,700" rel="stylesheet" type="text/css">
    <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/7cd93c2/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/5c0d9a6/css/base.css" />
    <script type="text/javascript" src="https://img.atcoder.jp/public/5c0d9a6/js/lib/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="https://img.atcoder.jp/public/5c0d9a6/js/lib/bootstrap.min.js"></script>
    <script>const rating_history = {rating_history}</script>
  </head>
  <body>
    <div id="main-container" class="container" >
    <div class="row">

    <div class="col-md-3 col-sm-12">
      <h3>
        <b>{profile['rank']}</b><br>
        <img src="../assets/flag32_{profile['flag']}.png"> <img src="../assets/crown_champion.png"> <a href="#" class="username"><span class="user-red">{profile['username']}</span></a> <img class="fav-btn" src="../assets/fav.png" width="16px" data-name="jokowi">
      </h3>
      <img class="avatar" src="../assets/{profile['username']}.jpg" width="128" height="128">

        <table class="dl-table">
        <tbody><tr><th class="no-break">Country/Region</th><td><img src="../assets/flag_{profile['flag']}.png"> {profile['region']}</td></tr>
        <tr><th class="no-break">Birth Year</th><td>{profile['birth']}</td></tr>
        <tr><th class="no-break">Twitter ID</th><td><a href="https://twitter.com/{profile['username']}" target="_blank">@{profile['username']}</a></td></tr>
        <tr><th class="no-break">Affiliation</th><td class="break-all">{profile['affiliation']}</td></tr>
        </tbody></table>

        <p><b>Win</b><span class="glyphicon glyphicon-question-sign" aria-hidden="true" data-html="true" data-toggle="tooltip" title="" data-original-title="Only contests without rating upperbound"></span> {profile['wins']}</p>
        {'<img class="avatar" src="../assets/{}.jpg" width="32" height="32">'.format(profile['username']) * profile['wins']}
    </div>

    <div class="col-md-9 col-sm-12">
      <h3>COVID-19 Status</h3>
      <hr/>
      <table class="dl-table">
        <tbody>
          <tr><th class="no-break">Rank</th><td>1st</td></tr>
          <tr><th class="no-break">Rating</th><td><span class="user-{get_rating_color(rating_stats['CurrentRating'])}">{rating_stats['CurrentRating']}</span></td></tr>
          <tr><th class="no-break">Highest Rating</th><td><span class="user-{get_rating_color(rating_stats['HighestRating'])}">{rating_stats['HighestRating']}</span><span class="gray"> &mdash; </span><span class="bold">{profile['current_rank']}</span><span class="gray"> (+{profile['to_promote']} to promote)</span></td></tr>
          <tr><th class="no-break">Rated Matches <span class="glyphicon glyphicon-question-sign" aria-hidden="true" data-html="true" data-toggle="tooltip" title="" data-original-title="Counts only rated contests"></span></th><td>{rating_stats['RatedMatches']}</td></tr>
          <tr><th class="no-break">Last Competed</th><td>{rating_stats['LastCompeted']}</td></tr>
        </tbody>
      </table>

      <div class="mt-2 mb-2" style="line-height: 0;">
        <link href="https://fonts.googleapis.com/css?family=Squada+One" rel="stylesheet" type="text/css" />
        <script type="text/javascript" src="https://code.createjs.com/easeljs-0.8.2.min.js"></script>
        <canvas id="ratingStatus" width="640" height="80"></canvas><br>
        <canvas id="ratingGraph" width="640" height="360"></canvas><br>
      </div>
    </div>

    </div>
    </div>

    <script type="text/javascript" src="https://img.atcoder.jp/public/5c0d9a6/js/rating-graph.js"></script>
    <script>$('[data-toggle="tooltip"]').tooltip();</script>

    <script type="application/javascript">
    var doNotTrack = false;
    if (!doNotTrack) {{
        (function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
        (i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        }})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
        ga('create', 'UA-153624663-1', 'auto');
        
        ga('send', 'pageview');
    }}
    </script>
  </body>
</html>
'''


if __name__ == '__main__':
    for country in ('SGP', 'IDN'):
        if not os.path.exists(country):
            os.makedirs(country)
        with open(os.path.join(country, 'index.html'), 'w') as fp:
            fp.write(get_html(country))
