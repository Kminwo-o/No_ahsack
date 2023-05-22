from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import (require_http_methods, require_POST,
                                          require_safe)

# from django.db.models import Movie
from .forms import PostSearchForm
from .models import Movie


# Create your views here.
@require_http_methods(['GET', 'POST'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie
    }
    return render(request, 'movies/detail.html', context)


@require_http_methods(['POST'])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.users.filter(pk=user.pk).exists():
        movie.users.remove(user)
        # is_liked = False
    else:
        movie.users.add(user)
        # is_liked = True
    # like_count = review.like_users.count()
    # context = {
    #     'is_liked': is_liked,
    #     'like_count': like_count
    # }

    return redirect('movies:detail', movie_pk)


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
            if search_query.lower() in movie.title.lower():  # 검색어가 영화 제목에 포함되는지 확인
                matched_movies.append(movie)  # 부분일치하는 영화 제목을 리스트에 추가

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
                        print(f'좋아요 목록 : {like_movie_id}')
                        print(f'영화 id : {movie.movie_id}')
                        recommand_movie.add(movie)

                        # 추천 하고 싶은 영화 개수
                        if len(recommand_movie) >= 4:
                            context = {
                                'form': form,
                                'like_movie': like_movie,
                                'recommand_movie': recommand_movie,
                                'matched_movies': matched_movies,
                            }
                            return render(request, 'movies/index.html', context)
        else:
            context = {
                'form': form,
                'like_movie': like_movie,
                'recommand_movie': recommand_movie,
                'matched_movies': matched_movies,
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

        recommand_movie = set()
        for key in director_lst:
            for movie in movie_data:
                if key[0] == movie.director:
                    if movie.movie_id not in like_movie_id:
                        print(f'좋아요 목록 : {like_movie_id}')
                        print(f'영화 id : {movie.movie_id}')
                        recommand_movie.add(movie)

                        # 추천 하고 싶은 영화 개수
                        if len(recommand_movie) >= 4:
                            context = {
                                'form': form,
                                'like_movie': like_movie,
                                'recommand_movie': recommand_movie
                            }
                            return render(request, 'movies/index.html', context)

        else:
            context = {
                'form': form,
                'like_movie': like_movie,
                'recommand_movie': recommand_movie
            }
        return render(request, 'movies/index.html', context)
