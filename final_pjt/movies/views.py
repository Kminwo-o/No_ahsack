from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import (require_http_methods, require_POST,
                                          require_safe)
from django.http import JsonResponse
# from django.db.models import Movie
from .forms import PostSearchForm
from .models import Movie
import random
from jamo import h2j, j2hcj

# Create your views here.
@require_http_methods(['GET', 'POST'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def movie_like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        
        if movie.users.filter(pk=user.pk).exists():
            movie.users.remove(user)
            is_liked = False
        else:
            movie.users.add(user)
            is_liked = True
        # like_count = movie.users.count()
        context = {
            'is_liked': is_liked,
            # 'like_count': like_count
        }
        return JsonResponse(context)
        # return redirect('community:index')
    return redirect('accounts:login')

@require_http_methods(['GET', 'POST'])
def index(request):
    # 로그인이 만약 안되어있으면
    # 메세지 하나 띄우고 로그인하세용
    # 로그인 창으로 쫒아내기

    # movies/index에 들어오면 우선
    # DB의 Movie 에서 title 값들을 가져와서 movie_titles에 할당합니다.
    movie_data = Movie.objects.all()

    form = PostSearchForm()
    user = request.user
    if request.method == 'POST':
        search_query = request.POST.get('search_word')  # POST 요청에서 검색어 가져오기
        matched_movies = []  # 부분일치하는 영화 제목을 담을 빈 리스트 초기화

        for movie in movie_data:
            matched_consonant = []
            for i in range(len(search_query)):
                # 검색어가 영화 제목에 포함되는지 확인
                if search_query[i].lower() not in movie.title.lower():
                    break
            else:
                matched_movies.append(movie)  # 부분일치하는 영화 제목을 리스트에 추가

            # 초성 검색
            for i in movie.title.lower():
                jamo_str = j2hcj(h2j(i))
                matched_consonant.append(jamo_str[0])

            m_n = "".join(matched_consonant)

            if search_query.lower() in m_n.lower():
                if movie not in matched_movies:
                    matched_movies.append(movie)
        # 추천 영화리스트
        director_lst = dict()
        like_movie = user.movie_set.all()
        like_movie_id = set()
        for movie in like_movie:
            if movie.director not in director_lst:
                director_lst[movie.director] = 1
                like_movie_id.add(movie.movie_id)
            else:
                director_lst[movie.director] += 1
                like_movie_id.add(movie.movie_id)
        # 높은 순으로 정렬된 영화 감독 이름
        director_lst = sorted(director_lst.items(),
                              key=lambda x: x[1], reverse=True)

        recommand_movie = set()
        for key in director_lst:
            for movie in movie_data:
                if key[0] == movie.director:
                    if movie.movie_id not in like_movie_id:

                        recommand_movie.add(movie)

                        # 추천 하고 싶은 영화 개수
                        if len(recommand_movie) >= 4:
                            context = {
                                'form': form,
                                'like_movie': like_movie,
                                'recommand_movie': recommand_movie,
                                'matched_movies': matched_movies,
                                'search_value': search_query,
                            }
                            return render(request, 'movies/index.html', context)
        else:
            context = {
                'form': form,
                'like_movie': like_movie,
                'recommand_movie': recommand_movie,
                'matched_movies': matched_movies,
                'search_value': search_query,
            }

        return render(request, 'movies/index.html', context)

    else:
        director_lst = dict()
        like_movie = user.movie_set.all()
        like_movie_id = set()
        for movie in like_movie:
            if movie.director not in director_lst:
                director_lst[movie.director] = 1
                like_movie_id.add(movie.movie_id)
            else:
                director_lst[movie.director] += 1
                like_movie_id.add(movie.movie_id)
                
        # 높은 순으로 정렬된 영화 감독 이름
        director_lst = sorted(director_lst.items(),
                              key=lambda x: x[1], reverse=True)

        recommand_movie = []
        for key in director_lst:
            for movie in movie_data:
                if key[0] == movie.director:
                    if movie.movie_id not in like_movie_id and movie not in recommand_movie:
                        recommand_movie.append(movie)

        else:
            random.shuffle(recommand_movie)
            context = {
                'form': form,
                'like_movie': like_movie,
                'recommand_movie': recommand_movie[:4]
            }

        return render(request, 'movies/index.html', context)