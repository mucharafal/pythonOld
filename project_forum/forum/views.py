from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User, Group

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from unicodedata import normalize

import datetime

from .models import Forum, Thread, Post
from .forms import AddPost, AddForum, AddThread, AddUser

import re


# Create your views here.

def normalize_slug(name):
    return normalize('NFD', (str.lower(name).replace(" ", "-"))).encode('ASCII', 'ignore').decode('utf-8')


def get_path(forum):
    if forum.pk == forum.forum.pk:
        return "forum/"
    else:
        return get_path(Forum.objects.get(pk=forum.forum.pk)) + forum.slug + "/"


def redirect_to(links):
    re_expression = links[0]
    link = links[1]

    def decorator(f):
        def wrapper(request):
            if re.match(re_expression, request.path):
                response = redirect(link)
            else:
                response = f(request)
            return response

        return wrapper

    return decorator


def check_permission_decorator(function):
    def wrapper(request):
        parent = get_parent(request)

        uid = request.session.get('_auth_user_id')
        if uid == None:
            return redirect('/register')
        user = User.objects.get(id=uid)

        print(check_permission(user, parent))
        if check_permission(user, parent):
            return function(request)
        else:
            return redirect("/forum")
    return wrapper


def check_permission(user, forum):
    return user.groups.filter(pk=forum.group.pk).exists()


def get_parent(request):
    path = request.path
    sliced_path = path.rsplit(sep="/")[1:]
    parent = list(Forum.objects.filter(id=1))
    parent = parent[0]
    for slug in sliced_path[1:]:
        if slug and not re.search('.thread', slug):
            parent = list(Forum.objects.filter(forum_id=parent.id, slug=slug))
            parent = parent[0]
    return parent


def show_thread(request):
    parent = get_parent(request)
    path = request.path
    thread_name = list(filter(lambda x: x, path.rsplit(sep="/")[1:]))[-1][:-1 * len(".thread")]
    thread = Thread.objects.filter(forum_id=parent.id, slug=thread_name)
    thread = thread[0]
    posts = Post.objects.filter(thread_id=thread.id)

    proposed_text = "Your text"
    form = AddPost(initial={'post_text': proposed_text, })

    add_post_link = "/posts/" + str(thread.pk) + "/add/"

    return render(request, 'forum/show_posts.html', {'title': parent.title, 'posts': posts,
                                                     'add_post_link': add_post_link, 'form': form})


@check_permission_decorator
def show_forum(request):
    parent = get_parent(request)
    path = request.path

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    subforums = list(Forum.objects.filter(forum_id=parent.id))
    subforums = filter(lambda forum: check_permission(user, forum), subforums)
    subforums = list(map(lambda element: (element, path + "/" + element.slug), subforums))
    threads = list(Thread.objects.filter(forum_id=parent.id))
    threads = list(map(lambda element: (element, path + "/" + element.slug + ".thread"), threads))
    subobjects = subforums + threads

    proposed_text = "Thread title"
    thread_form = AddThread(initial={'title': proposed_text, })
    add_thread_link = "/threads/" + str(parent.pk) + "/add/"

    groups = map(lambda group: (group.pk, group.name), user.groups.all())
    print(groups)
    forum_form = AddForum(initial={'title': proposed_text, }, groups=groups)
    add_forum_link = "/forums/" + str(parent.pk) + "/add/"

    return render(request, 'forum/show_subobjects.html', {'title': parent.title, 'subforums': subobjects,
                                                          'forum_form': forum_form, 'thread_form': thread_form,
                                                          'add_forum_link': add_forum_link, 'add_thread_link': add_thread_link})


@check_permission_decorator
@redirect_to(("/index[.]*", "/forum"))
def index(request):
    subforums = Forum.objects.filter(~Q(id=1), forum_id=1)

    uid = request.session.get('_auth_user_id')

    user = User.objects.get(id=uid)

    subforums = filter(lambda forum: check_permission(user, forum), list(subforums))

    proposed_text = "Forum title"
    groups = map(lambda group: (group.pk, group.name), user.groups.all())
    print(groups)
    forum_form = AddForum(initial={'title': proposed_text, }, groups=groups)
    add_forum_link = "/forums/1/add/"

    path = request.path
    subobjects_with_path = []
    for subobject in subforums:
        subobjects_with_path = subobjects_with_path + [(subobject, path + subobject.slug)]
    return render(request, 'forum/show_subobjects.html', {'title': "Główne forum", "subforums": subobjects_with_path,
                                                          'forum_form': forum_form, 'add_forum_link': add_forum_link})


def add_post(request, pk):
    thread = get_object_or_404(Thread, pk = pk)

    # checking permission
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    forum = Forum.objects.get(pk=thread.forum.pk)
    path = get_path(forum)
    path = "/" + path + thread.slug + ".thread"

    print("Path" + path)
    if check_permission(user, forum):

        if request.method == 'POST':
            form = AddPost(request.POST)
            if form.is_valid():
                print("Saving")
                new_post = Post.objects.create(
                    author=user,
                    date=datetime.datetime.now(),
                    text=form.cleaned_data['post_text'],
                    thread=thread
                )
                new_post.save()

    return redirect(path)

def add_forum(request, pk):
    print("PK: " + str(pk))
    forum = get_object_or_404(Forum, pk=pk)

    # checking permission
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    groups = map(lambda group: (group.pk, group.name), user.groups.all())

    path = "/" + get_path(forum)

    print("Path" + path)
    if check_permission(user, forum):

        if request.method == 'POST':
            form = AddForum(request.POST, groups=groups)
            if form.is_valid():
                # wybierz grupę spośród grup użytkownika
                # nazwa forum
                print("Saving")
                new_forum = Forum.objects.create(
                    title=form.cleaned_data['title'],
                    slug=normalize_slug(form.cleaned_data['title']),
                    forum=forum,
                    group=Group.objects.get(pk=form.cleaned_data['group'])
                )
                new_forum.save()

    return redirect(path)

def add_thread(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    # checking permission
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    path = "/" + get_path(forum)

    print("Path" + path)
    if check_permission(user, forum):

        if request.method == 'POST':
            form = AddThread(request.POST)
            if form.is_valid():
                # wybierz grupę spośród grup użytkownika
                # nazwa forum
                print("Saving")
                new_thread = Thread.objects.create(
                    title=form.cleaned_data['title'],
                    slug=normalize_slug(form.cleaned_data['title']),
                    forum=forum,
                )
                new_thread.save()

    return redirect(path)

def register(request):
    if request.method == 'POST':
        form = AddUser(request.POST)
        if form.is_valid():
            User.objects.filter(username=form.cleaned_data['login']).exists()
            print("Adding new user")
            new_user = User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password']
            )
            main_group = Group.objects.get(name='MainForum')
            new_user.groups.add(main_group)
            new_user.save()
            return redirect("/accounts/login")
    else:
        register_form = AddUser(initial={'login': 'login', 'password': 'password'})
    return render(request, 'forum/register.html', {'register_form': register_form, })
