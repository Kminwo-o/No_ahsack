from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import (require_http_methods, require_POST,
                                          require_safe)

from .forms import CommentForm, ReviewForm
from .models import Comment, Review


@require_safe
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'community/index.html', context)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_safe
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
        
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_liked = False
        else:
            review.like_users.add(user)
            is_liked = True
        like_count = review.like_users.count()
        context = {
            'is_liked': is_liked,
            'like_count': like_count
        }
        return JsonResponse(context)
        
    return redirect('accounts:login')

@require_POST
def delete(request, review_pk):
    # 게시글 작성자와 로그인된 사용자가 같으면 삭제하도록 변경
    if request.user.is_authenticated:
        review = Review.objects.get(pk=review_pk)
        if review.user == request.user:
            review.delete()
    return redirect('community:index')

@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('community:detail', review_pk=review.pk)
        else:
            
            form = ReviewForm(instance=review)

        context = {'form': form, 'review': review}
        return render(request, 'community/update.html', context)
    else:
        return redirect('community:index')


