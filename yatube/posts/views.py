from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Comment, Follow
from .utils import paginator_func


def index(request):
    """View функция для index."""
    post_list = Post.objects.all()
    context = {
        'page_obj': paginator_func(request, post_list),
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """View функция для group_posts."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author')
    context = {
        'group': group,
        'page_obj': paginator_func(request, post_list),
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """View функция для profile."""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group')
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=author).exists()
    else:
        following = False
    context = {
        'author': author,
        'page_obj': paginator_func(request, post_list),
        'following': following,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """View функция для post_detail."""
    post = get_object_or_404(Post, pk=post_id)
    # comments = post.comments.all()
    comments = Comment.objects.filter(post_id=post_id)
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """View функция для создания записи."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('posts:profile', post.author)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """View функция для редактирования записи."""
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if request.user != post.author:

        return redirect('posts:post_detail', post_id=post_id)

    if form.is_valid():
        form.save()

        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'post_id': post_id,
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    """View функция для добавления комментариев."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """View функция для отображения подписок."""
    posts = Post.objects.filter(author__following__user=request.user)
    context = {
        'page_obj': paginator_func(request, posts),
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """View функция для того, чтобы подписаться."""
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()
    if request.user != author and not follower:
        follow = Follow.objects.create(
            user=request.user,
            author=author
        )
        follow.save()

    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """View функция для того, чтобы отписаться."""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
