import os
import django

from main_app.choices import TeamChoices
from main_app.models import FootballPlayer, FootballCoach, Team

# change the data info to: FootballPlayer / FootballCoach / Team

data =[
    {"fans":68193,"budget":5396257.68,"stadium":"Klocko-Lindgren"},
    {"fans":47230,"budget":6856714.28,"stadium":"Leuschke, Padberg and Barrows"},
    {"fans":17058,"budget":601249.87,"stadium":"Kautzer-Conroy"},
    {"fans":11658,"budget":9395672.03,"stadium":"Morissette Group"},
    {"fans":31971,"budget":2126260.69,"stadium":"Effertz Inc"},
    {"fans":58353,"budget":5952874.15,"stadium":"Runolfsdottir, Towne and Lemke"},
    {"fans":41358,"budget":1407069.66,"stadium":"Rice, Williamson and Baumbach"},
    {"fans":31962,"budget":1605432.18,"stadium":"Cole and Sons"},
    {"fans":96805,"budget":6502631.18,"stadium":"Bartell-Kunde"},
    {"fans":56741,"budget":1224143.85,"stadium":"Gorczany and Sons"},
    {"fans":48615,"budget":1425794.26,"stadium":"Dietrich-Morissette"},
    {"fans":98207,"budget":2738640.84,"stadium":"Jenkins, McDermott and Jacobs"},
    {"fans":49631,"budget":1677037.83,"stadium":"Grimes and Sons"},
    {"fans":29974,"budget":1758064.47,"stadium":"Gutmann, King and MacGyver"},
    {"fans":43088,"budget":2144941.9,"stadium":"Okuneva, Fadel and Hackett"},
    {"fans":46419,"budget":8749141.69,"stadium":"Brown, Runte and Runte"},
    {"fans":40331,"budget":6899645.43,"stadium":"Romaguera LLC"},
    {"fans":10033,"budget":4465326.48,"stadium":"Prosacco Group"},
    {"fans":73815,"budget":1720676.84,"stadium":"Auer-Cassin"},
    {"fans":29685,"budget":8345085.7,"stadium":"Hessel, Nienow and Wunsch"},
    {"fans":45808,"budget":1770019.28,"stadium":"Powlowski, Sipes and Pagac"},
    {"fans":28502,"budget":2705653.56,"stadium":"Lowe and Sons"},
    {"fans":41640,"budget":6528786.63,"stadium":"Wehner, Deckow and Reichert"},
    {"fans":89613,"budget":2343106.56,"stadium":"Schaden-DuBuque"},
    {"fans":26419,"budget":6700692.69,"stadium":"Rath LLC"},
    {"fans":71438,"budget":7186293.7,"stadium":"Luettgen, Wintheiser and Abernathy"},
    {"fans":54138,"budget":7204639.15,"stadium":"Larson Group"},
    {"fans":12191,"budget":5274417.23,"stadium":"Torp, MacGyver and Cormier"},
    {"fans":91698,"budget":6579406.43,"stadium":"Purdy-Rolfson"},
    {"fans":85653,"budget":4590574.87,"stadium":"Becker-Goyette"},
    {"fans":59241,"budget":2323499.36,"stadium":"Wilderman, Durgan and Murazik"},
    {"fans":29379,"budget":2302233.48,"stadium":"Bruen Inc"},
    {"fans":82405,"budget":4506719.3,"stadium":"Schuppe-Botsford"},
    {"fans":97415,"budget":5013255.86,"stadium":"Gleason Group"},
    {"fans":25117,"budget":7472656.87,"stadium":"Steuber-Balistreri"},
    {"fans":66973,"budget":7214458.4,"stadium":"Bahringer Inc"},
    {"fans":46193,"budget":6113191.61,"stadium":"Reinger, Sauer and Schowalter"},
    {"fans":90103,"budget":619676.52,"stadium":"Kautzer and Sons"},
    {"fans":18092,"budget":1793200.45,"stadium":"Steuber-Wunsch"},
    {"fans":15089,"budget":6447321.38,"stadium":"Bernier, Rowe and Considine"}
]


def populate_func():
    for d in data:
        team = Team.objects.create(
            fans=d['fans'],
            budget=d['budget'],
            stadium=d['stadium'],
        )
        team.save()

    return 'Population done!'
