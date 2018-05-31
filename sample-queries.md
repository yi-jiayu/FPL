# Sample queries

## Top players, club, position and price overall

```sql
select
  p.web_name,
  t.name as club,
  r.singular_name_short as position,
  p.total_points,
  (p.now_cost / 10.0) as price
from players p
  left join teams t on p.team = t.id
  left join roles r on p.element_type = r.id
order by total_points
  desc
limit 20;
```

| web_name    |      club | position | total_points | price |
|:------------|:----------|:---------|-------------:|------:|
| Salah       | Liverpool |      MID |          303 |  10.6 |
| Sterling    |  Man City |      MID |          229 |   9.1 |
| Kane        |     Spurs |      FWD |          217 |  13.1 |
| De Bruyne   |  Man City |      MID |          209 |  10.3 |
| Eriksen     |     Spurs |      MID |          199 |   9.7 |
| Mahrez      | Leicester |      MID |          195 |   8.7 |
| Vardy       | Leicester |      FWD |          183 |   8.8 |
| Firmino     | Liverpool |      FWD |          181 |   9.5 |
| Sané        |  Man City |      MID |          179 |   8.7 |
| Son         |     Spurs |      MID |          178 |   8.3 |
| Azpilicueta |   Chelsea |      DEF |          175 |   6.9 |
| Alli        |     Spurs |      MID |          175 |     9 |
| Hazard      |   Chelsea |      MID |          173 |  10.5 |
| De Gea      |   Man Utd |      GKP |          172 |   5.9 |
| David Silva |  Man City |      MID |          169 |   8.2 |
| Agüero      |  Man City |      FWD |          169 |  11.5 |
| Alonso      |   Chelsea |      DEF |          165 |   7.1 |
| Groß        |  Brighton |      MID |          164 |   5.9 |
| Lukaku      |   Man Utd |      FWD |          162 |  11.5 |
| Ederson     |  Man City |      GKP |          158 |   5.7 |

## Top players, club and position by gameweek

```sql
select
  p.web_name,
  t.name                as club,
  r.singular_name_short as position,
  pmd.round             as gameweek,
  max(pmd.total_points) as points
from players p
  left join teams t on p.team = t.id
  left join roles r on p.element_type = r.id
  left join player_match_details pmd on p.id = pmd.element
group by gameweek
order by gameweek
  asc;
```

| web_name    | club           | position | gameweek | points |
|:------------|:---------------|:---------|---------:|-------:|
| Hegazi      | West Brom      |      DEF |        1 |     15 |
| Alonso      | Chelsea        |      DEF |        2 |     16 |
| Clark       | Newcastle      |      DEF |        3 |     15 |
| Groß        | Brighton       |      MID |        4 |     18 |
| Agüero      | Man City       |      FWD |        5 |     20 |
| Morata      | Chelsea        |      FWD |        6 |     17 |
| Fellaini    | Man Utd        |      MID |        7 |     16 |
| Sterling    | Man City       |      MID |        8 |     15 |
| Kane        | Spurs          |      FWD |        9 |     16 |
| Kolasinac   | Arsenal        |      DEF |       10 |     14 |
| Steve Cook  | Bournemouth    |      DEF |       11 |     15 |
| Hazard      | Chelsea        |      MID |       12 |     18 |
| Zeegelaar   | Watford        |      DEF |       13 |     14 |
| Özil        | Arsenal        |      MID |       14 |     17 |
| Coutinho    | Liverpool      |      MID |       15 |     18 |
| Son         | Spurs          |      MID |       16 |     16 |
| Willian     | Chelsea        |      MID |       17 |     16 |
| Mooy        | Huddersfield   |      MID |       18 |     15 |
| Kane        | Spurs          |      FWD |       19 |     17 |
| Kane        | Spurs          |      FWD |       20 |     17 |
| Willian     | Chelsea        |      MID |       21 |     17 |
| Mahrez      | Leicester      |      MID |       22 |     14 |
| Arnautovic  | West Ham       |      MID |       23 |     16 |
| Moses       | Chelsea        |      DEF |       24 |     17 |
| Walcott     | Everton        |      MID |       25 |     15 |
| Ramsey      | Arsenal        |      MID |       26 |     20 |
| Agüero      | Man City       |      FWD |       27 |     21 |
| Ederson     | Man City       |      GKP |       28 |     15 |
| Son         | Spurs          |      MID |       29 |     16 |
| Kenedy      | Newcastle      |      MID |       30 |     16 |
| Salah       | Liverpool      |      MID |       31 |     29 |
| Arnautovic  | West Ham       |      MID |       32 |     16 |
| Welbeck     | Arsenal        |      FWD |       33 |     16 |
| Moses       | Chelsea        |      DEF |       34 |     14 |
| Lacazette   | Arsenal        |      FWD |       35 |     13 |
| Tadic       | Southampton    |      MID |       36 |     15 |
| Aubameyang  | Arsenal        |      FWD |       37 |     16 |
| van Aanholt | Crystal Palace |      DEF |       38 |     18 |

## Top scoring player from each club

```sql
select
  p.web_name,
  t.name                as club,
  r.singular_name_short as position,
  max(p.total_points)   as total_points
from players p left join teams t on p.team = t.id
  left join roles r on p.element_type = r.id
group by p.team;
```

| web_name    | club           | position | total_points | cost |
|:------------|:---------------|:---------|-------------:|-----:|
| Salah       | Liverpool      | MID      |          303 | 10.6 |
| Sterling    | Man City       | MID      |          229 |  9.1 |
| Kane        | Spurs          | FWD      |          217 | 13.1 |
| Mahrez      | Leicester      | MID      |          195 |  8.7 |
| Azpilicueta | Chelsea        | DEF      |          175 |  6.9 |
| De Gea      | Man Utd        | GKP      |          172 |  5.9 |
| Groß        | Brighton       | MID      |          164 |  5.9 |
| Fabianski   | Swansea        | GKP      |          157 |  4.7 |
| Shaqiri     | Stoke          | MID      |          155 |  6.1 |
| Pope        | Burnley        | GKP      |          152 |    5 |
| Pickford    | Everton        | GKP      |          145 |  4.9 |
| Milivojevic | Crystal Palace | MID      |          144 |  5.2 |
| Arnautovic  | West Ham       | MID      |          144 |  7.1 |
| Lacazette   | Arsenal        | FWD      |          138 | 10.3 |
| Doucouré    | Watford        | MID      |          136 |  5.2 |
| Lössl       | Huddersfield   | GKP      |          135 |  4.6 |
| Pérez       | Newcastle      | FWD      |          124 |  5.5 |
| Foster      | West Brom      | GKP      |          123 |  4.3 |
| Tadic       | Southampton    | MID      |          122 |  6.2 |
| Begovic     | Bournemouth    | GKP      |          112 |  4.5 |

## Clubs by away, home and total goals scored
```sql
select
  t.name as club,
  sum(f.team_a_score) + h.home_goals as total_goals,
  sum(f.team_a_score)                as away_goals,
  h.home_goals
from teams t left join fixtures f on t.id = f.team_a
  left join (select
               t2.id,
               sum(f2.team_h_score) as home_goals
             from teams t2 left join fixtures f2 on t2.id = f2.team_h
             group by t2.id) h on h.id = t.id
group by t.id
order by total_goals
  desc;
 ```
 
| club           | total_goals | away_goals | home_goals |
|:---------------|------------:|-----------:|-----------:|
| Man City       | 106         | 45         | 61         |
| Liverpool      | 84          | 39         | 45         |
| Arsenal        | 74          | 20         | 54         |
| Spurs          | 74          | 34         | 40         |
| Man Utd        | 68          | 30         | 38         |
| Chelsea        | 62          | 32         | 30         |
| Leicester      | 56          | 31         | 25         |
| West Ham       | 48          | 24         | 24         |
| Bournemouth    | 45          | 19         | 26         |
| Crystal Palace | 45          | 16         | 29         |
| Everton        | 44          | 16         | 28         |
| Watford        | 44          | 17         | 27         |
| Newcastle      | 39          | 18         | 21         |
| Southampton    | 37          | 17         | 20         |
| Burnley        | 36          | 20         | 16         |
| Stoke          | 35          | 15         | 20         |
| Brighton       | 34          | 10         | 24         |
| West Brom      | 31          | 10         | 21         |
| Huddersfield   | 28          | 12         | 16         |
| Swansea        | 28          | 11         | 17         |

## Gameweek differentials

```sql
select
  p.web_name,
  pmd.round as gameweek,
  pmd.selected,
  pmd.total_points
from players p left join
  player_match_details pmd on p.id = pmd.element
where pmd.selected > 0 and pmd.selected < 10000 and pmd.total_points > 10
order by pmd.selected
  asc;
```

| web_name      | gameweek | selected | total_points |
|---------------|---------:|---------:|-------------:|
| Pritchard     |       27 |      666 |           12 |
| Clucas        |       25 |     1629 |           15 |
| Ki Sung-yueng |       27 |     2198 |           11 |
| Gosling       |       20 |     3110 |           12 |
| Zeegelaar     |       13 |     3300 |           14 |
| Stanislas     |        9 |     4395 |           13 |
| Malone        |       11 |     5592 |           12 |
| Hughes        |       12 |     5642 |           14 |
| Stanislas     |       25 |     6404 |           12 |
| Wilson        |       12 |     6520 |           17 |
| João Mário    |       37 |     7162 |           11 |
| Choupo-Moting |        4 |     7609 |           15 |
| Murray        |        9 |     7880 |           13 |
| Lamela        |       38 |     8618 |           16 |
| Richarlison   |        2 |     8884 |           11 |
| Arfield       |       16 |     9570 |           11 |

## Overall differentials

```sql
select
  p.web_name,
  p.total_points,
  p.selected_by_percent
from players p
where selected_by_percent > 0 and total_points > 150
order by selected_by_percent
  asc;
```

| web_name    | club      | position | total_points | selected_by_percent | price |
|-------------|-----------|----------|-------------:|--------------------:|------:|
| Sánchez     | Man Utd   | MID      |          152 |                   3 |  11.4 |
| Hazard      | Chelsea   | MID      |          173 |                 6.4 |  10.5 |
| Mahrez      | Leicester | MID      |          195 |                 8.2 |   8.7 |
| Shaqiri     | Stoke     | MID      |          155 |                 8.6 |   6.1 |
| Ederson     | Man City  | GKP      |          158 |                   9 |   5.7 |
| Fabianski   | Swansea   | GKP      |          157 |                10.1 |   4.7 |
| Pope        | Burnley   | GKP      |          152 |                10.1 |     5 |
| Agüero      | Man City  | FWD      |          169 |                10.7 |  11.5 |
| David Silva | Man City  | MID      |          169 |                11.5 |   8.2 |
| Sané        | Man City  | MID      |          179 |                13.4 |   8.7 |
| Alli        | Spurs     | MID      |          175 |                13.8 |     9 |
| Son         | Spurs     | MID      |          178 |                  14 |   8.3 |
| Groß        | Brighton  | MID      |          164 |                15.4 |   5.9 |
| Alonso      | Chelsea   | DEF      |          165 |                16.2 |   7.1 |
| Eriksen     | Spurs     | MID      |          199 |                19.4 |   9.7 |
| Azpilicueta | Chelsea   | DEF      |          175 |                  21 |   6.9 |
| De Bruyne   | Man City  | MID      |          209 |                21.4 |  10.3 |
| Vardy       | Leicester | FWD      |          183 |                21.7 |   8.8 |
| Lukaku      | Man Utd   | FWD      |          162 |                21.9 |  11.5 |
