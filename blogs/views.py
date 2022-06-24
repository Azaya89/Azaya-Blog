from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import BlogPost, Entry
from .forms import BlogForm, EntryForm

def index(request):
    """The home page for Blog."""
    return render(request, 'blogs/index.html')

def register_error(request):
    """Show an error page."""
    return render(request, 'blogs/register_error.html')

def posts(request):
    """Show all posts."""
    posts = BlogPost.objects.order_by('date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

def post(request, post_id):
    """Show a single post and all its entries."""
    post = BlogPost.objects.get(id=post_id)
    entries = post.entry_set.order_by('-date_added')
    context = {'post': post, 'entries': entries}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    """Add a new blog post."""
    if request.method != 'POST':
    # No data submitted, create a blank form.
        form = BlogForm()
    else:
    # POST data submitted; process data.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
        return redirect('blogs:posts')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def new_entry(request, post_id):
    """Add a new entry for a particular blog post."""
    post = BlogPost.objects.get(id=post_id)
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
    # No data submitted; create a blank form.
        form = EntryForm()
    else:
    # Post data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = post
            new_entry.save()
            return redirect('blogs:post', post_id=post_id)

    # Display a blank or invalid form.
    context = {'post': post, 'form': form}
    return render(request, 'blogs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    post = entry.topic
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
    #Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
    # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('blogs:post', post_id=post.id)

    context = {'entry': entry, 'post': post, 'form': form}
    return render(request, 'blogs/edit_entry.html', context)