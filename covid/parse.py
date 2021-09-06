# Data from https://docs.google.com/spreadsheets/d/1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw/htmlview#

import csv
import datetime
import json


FIRST_CONTEST_DATE = datetime.datetime(year=2020, month=3, day=3)


def get_rating_history():
    rating_history = []
    old_rating = 0
    current_day = FIRST_CONTEST_DATE
    with open('data.tsv') as fp:
        reader = csv.DictReader(fp, delimiter='\t')
        for row in reader:
            new_rating = int(row['Meninggal (baru)'].replace(',', ''))
            rating_history.append({
                'ContestName': 'Indonesia New COVID-19 Death',
                'OldRating': old_rating,
                'NewRating': new_rating,
                'EndTime': int(datetime.datetime.timestamp(current_day)),
                'Place': 1,
                'StandingsUrl': '#',
            })
            old_rating = new_rating
            current_day += datetime.timedelta(days=1)

    return rating_history


def get_rating_stats(rating_history):
    stats = {
        'CurrentRating': rating_history[-1]['NewRating'],
        'HighestRating': max(rating['NewRating'] for rating in rating_history),
        'RatedMatches': len(rating_history),
    }
    last_competed = FIRST_CONTEST_DATE + datetime.timedelta(days=stats['RatedMatches'] - 1)
    last_competed = '{:04d}/{:02d}/{:02d}'.format(last_competed.year, last_competed.month, last_competed.day)
    stats['LastCompeted'] = last_competed
    return stats


def get_html():
    # These still need to be manually modified: current rating color, highest rating color, rank, delta needed to promote
    rating_history = get_rating_history()
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
  <body style="display: flex; justify-content: center; align-items: center;">
    <div id="main-container" class="container" >
    <div class="row">

    <div class="col-md-3 col-sm-12">
      <h3>
        <b>President</b><br>
        <img src="assets/flag32_ID.png"> <img src="assets/crown_champion.png"> <a href="#" class="username"><span class="user-red">jokowi</span></a> <img class="fav-btn" src="assets/fav.png" width="16px" data-name="jokowi">
      </h3>
      <img class="avatar" src="assets/jokowi.jpg" width="128" height="128">

        <table class="dl-table">
        <tbody><tr><th class="no-break">Country/Region</th><td><img src="assets/flag_ID.png"> Indonesia</td></tr>
        <tr><th class="no-break">Birth Year</th><td>1961</td></tr>
        <tr><th class="no-break">Twitter ID</th><td><a href="https://twitter.com/jokowi" target="_blank">@jokowi</a></td></tr>
        <tr><th class="no-break">Affiliation</th><td class="break-all">Pancasila</td></tr>
        </tbody></table>

        <p><b>Win</b><span class="glyphicon glyphicon-question-sign" aria-hidden="true" data-html="true" data-toggle="tooltip" title="" data-original-title="Only contests without rating upperbound"></span> 2</p>
        <img class="avatar" src="assets/jokowi.jpg" width="32" height="32"><img class="avatar" src="assets/jokowi.jpg" width="32" height="32">
    </div>

    <div class="col-md-9 col-sm-12">
      <h3>COVID-19 Death Status</h3>
      <hr/>
      <table class="dl-table">
        <tbody>
          <tr><th class="no-break">Rank</th><td>1st</td></tr>
          <tr><th class="no-break">Rating</th><td><span class="user-gray">{rating_stats['CurrentRating']}</span></td></tr>
          <tr><th class="no-break">Highest Rating</th><td><span class="user-yellow">{rating_stats['HighestRating']}</span><span class="gray"> &mdash; </span><span class="bold">1 Dan</span><span class="gray">(+131 to promote)</span></td></tr>
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
    with open('index.html', 'w') as fp:
        fp.write(get_html())
