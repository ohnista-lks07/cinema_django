import django, os
from django.tasks.signals import task_started

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')
django.setup()
from movies.models import Genre, Director, Movie, Review
from django.db.models import Count, Avg, Min, Max, Q, F
#task1
movie = Movie.objects.all()
print("Movie : ", movie)
"""<QuerySet [<Movie: The Dark Knight (2008)>, <Movie: Pulp Fiction (1994)>, <Movie: Inception (2010)>,
 <Movie: Interstellar (2014)>, <Movie: Django Unchained (2012)>, <Movie: Parasite (2019)>, <Movie: Inglourious Basterds (2009)>,
  <Movie: The Grand Budapest Hotel (2014)>, <Movie: Blade Runner 2049 (2017)>, <Movie: Dune (2021)>, <Movie: Arrival (2016)>, <Movie: TeenWolf (2011)>, 
  <Movie: Tenet (2020)>]>"""
print("\nList movie : ",Movie.objects.values_list("title", flat=True))
"""<QuerySet ['The Dark Knight', 'Pulp Fiction', 'Inception', 
'Interstellar', 'Django Unchained', 'Parasite', 'Inglourious Basterds',
 'The Grand Budapest Hotel', 'Blade Runner 2049', 'Dune', 'Arrival', 'TeenWolf', 'Tenet']>"""


Movie.objects.values_list("duration", flat=True)
"""QuerySet [152, 154, 148, 169, 165, 132, 153, 99, 164, 155, 116, 150, 150]"""

#2
print('\ntask2')
print(Movie.objects.filter(rating__gte=8.5).order_by("-rating"))
""" [<Movie: The Dark Knight (2008)>, <Movie: Pulp Fiction (1994)>, <Movie: Inception (2010)>,
 <Movie: Interstellar (2014)>, <Movie: Django Unchained (2012)>, <Movie: Parasite (2019)>]>
"""
#3
print('\ntask3')
from django.db.models import Q
result = Movie.objects.filter(Q(title__icontains="Blade") | Q(title__icontains="Dark"))
print(result)
"QuerySet [<Movie: The Dark Knight (2008)>, <Movie: Blade Runner 2049 (2017)>]"

#4
print('\ntask4')
nolan_films = Movie.objects.filter(director__last_name="Nolan")
print(nolan_films)
"""[<Movie: The Dark Knight (2008)>, <Movie: Inception (2010)>, <Movie: Interstellar (2014)>, <Movie: Tenet (2020)>]>"""
#5
print('\ntask5')
print(Movie.objects.filter(genre__name="Sci-Fi", year__gt=2015).order_by("year"))
"""[<Movie: Arrival (2016)>, <Movie: Blade Runner 2049 (2017)>, <Movie: Dune (2021)>]"""

#6
print('\ntask6')
result = Movie.objects.exclude(
    Q(genre__name="Drama") | Q(genre__name="Comedy")
)
for m in result:
    print(m.title, "—", m.genre.name if m.genre else "без жанру")
    """The Dark Knight — Thriller
Pulp Fiction — Crime
Interstellar — Sci-Fi
Parasite — Crime
Django Unchained — Crime
Dune — Sci-Fi
Blade Runner 2049 — Sci-Fi
Arrival — Sci-Fi
TeenWolf — Sci-Fi
Tenet — Thriller"""


#7
print('\ntask7')
by_rating = Movie.objects.order_by("-rating")

# Сторінка 1
page1 = by_rating[:4]
for m in page1:
    print(m.title, m.rating)
"""The Dark Knight 9.0
Pulp Fiction 8.9
Inception 8.8
Interstellar 8.6"""

# Сторінка 2
page2 = by_rating[4:8]
for m in page2:
    print(m.title, m.rating)
"""Django Unchained 8.5
Parasite 8.5
Inglourious Basterds 8.3
The Grand Budapest Hotel 8.1"""


#8
print('\ntask8')
from django.db.models import Count

genres = Genre.objects.annotate(
    movie_count=Count("movie")
).order_by("-movie_count")

for g in genres:
    print(g.name, ":", g.movie_count)
""" Sci-Fi : 5
Crime : 3
Thriller : 2
Drama : 2
Comedy : 1"""


#9
print('\ntask9')
from django.db.models import Avg

# Загальний середній
total_avg = Movie.objects.aggregate(avg=Avg("rating"))
print("Середнiй рейтинг:", total_avg["avg"], '\n')
"""{'avg': Decimal('8.2769230769230769')}
Середнiй рейтинг: 8.2769230769230769"""

directors = Director.objects.annotate(
    avg_rating=Avg("movie__rating")
).values("last_name", "avg_rating").order_by("-avg_rating")
for d in directors:
    print(d["last_name"], ":", d["avg_rating"])
"""Tarantino : 8.5666666666666667
Joon-ho : 8.5000000000000000
Nolan : 8.4500000000000000
Anderson : 8.1000000000000000
Villeneuve : 7.9666666666666667
Malkey : 7.6000000000000000"""


#10
print('\ntask10')
no_reviews = Movie.objects.filter(review__isnull=True)
print(no_reviews)
""""<QuerySet [<Movie: The Dark Knight (2008)>, <Movie: Pulp Fiction (1994)>, 
<Movie: Interstellar (2014)>, <Movie: Django Unchained (2012)>, <Movie: Inglourious Basterds (2009)>,
 <Movie: The Grand Budapest Hotel (2014)>, <Movie: Dune (2021)>, <Movie: Blade Runner 2049 (2017)>,
  <Movie: Arrival (2016)>, <Movie: TeenWolf (2011)>]"""
#обидва запити дають однаковий вивід


#11
print('\ntask11')
updated_count = Movie.objects.filter(rating__lt=7.8).update(is_public=False)
print(f"Оновлено: {updated_count} фiльмiв")
"""Оновлено: 2 фiльмiв"""


#12
print('\ntask12')
from django.db.models import F

print(Movie.objects.filter(
    director__last_name="Tarantino"
).update(rating=F("rating") + 0.2))
"""3"""
print(Movie.objects.filter(director__last_name="Tarantino").values_list("title", "rating"))
"""('Pulp Fiction', Decimal('9.1')), ('Django Unchained', Decimal('8.7')), ('Inglourious Basterds', Decimal('8.5'))"""


#13
print('\ntask13')
inception = Movie.objects.get(title="Inception")

# Зворотній ForeignKey — review_set
reviews = inception.review_set.all()
for r in reviews:
    print(r.score, ":", r.text)

# Середня оцінка
avg_score = inception.review_set.aggregate(avg=Avg("score"))
print("Середня оцiнка:", avg_score["avg"])
"""Середня оцiнка: 9.5"""

#14
print('\ntask14')
from django.db.models import Avg
print(Director.objects.annotate(avg_rating=Avg("movie__rating")).order_by("-avg_rating").first())
"""Quentin Tarantino"""

#15
print('\ntask15')
print(Movie.objects.filter(rating__gt=8))
"""("[<Movie: Pulp Fiction (1994)>, <Movie: The Dark Knight (2008)>, <Movie: Inception (2010)>,"
 " <Movie: Django Unchained (2012)>, <Movie: Interstellar (2014)>, <Movie: Parasite (2019)>,"
 " <Movie: Inglourious Basterds (2009)>, <Movie: The Grand Budapest Hotel (2014)>")"""






