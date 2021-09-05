# Data from https://docs.google.com/spreadsheets/d/1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw/htmlview#

import csv
import datetime
import json
import os


FIRST_CONTEST_DATE = datetime.datetime(year=2020, month=3, day=2)


def get_rating_history():
    rating_history = []
    old_rating = 0
    current_day = FIRST_CONTEST_DATE
    with open(os.path.join('covid', 'data.tsv')) as fp:
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
    <link href="https://fonts.googleapis.com/css?family=Squada+One" rel="stylesheet" type="text/css" />
    <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/7cd93c2/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/5c0d9a6/css/base.css" />
    <script type="text/javascript" src="https://code.createjs.com/easeljs-0.8.2.min.js"></script>
    <script type="text/javascript" src="https://img.atcoder.jp/public/5c0d9a6/js/lib/jquery-1.9.1.min.js"></script>
    <script>const rating_history = {rating_history}</script>
  </head>
  <body style="display: flex; justify-content: center; align-items: center;">
    <div style="text-align: center">
      <h3>Indonesia COVID-19 Death Cases</h3>
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
        <canvas id="ratingStatus" width="640" height="80"></canvas><br>
        <canvas id="ratingGraph" width="640" height="360"></canvas><br>
      </div>

    </div>

    <script type="text/javascript" src="https://img.atcoder.jp/public/5c0d9a6/js/rating-graph.js"></script>
  </body>
</html>'''


if __name__ == '__main__':
    with open('covid.html', 'w') as fp:
        fp.write(get_html())
