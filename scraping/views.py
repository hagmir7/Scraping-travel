from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from base64 import encode
from bs4 import BeautifulSoup
import requests
from . models import Post, Page, Contact
from django.core.paginator import Paginator
from . forms import CreateContact, FormCreatePage
from django.contrib import messages

# Home page
def index(request):
    posts = Post.objects.all().order_by('-date')[0:24]
    context = {'posts': posts, 'title': "PoolsBox Travel Site"}
    return render(request, 'index.html', context)

#Travel page
def blog(request):
    content = Post.objects.all().order_by('-date')
    paginator = Paginator(content, 24) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts': posts, 'title': "PoolsBox Travel Site"}
    return render(request, 'blog.html', context)

# Post detail
def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views = post.views + 1
    post.save()
    posts = Post.objects.all().order_by('-date')[0:3]
    context = {'title': post.title, 'post': post, 'posts': posts}
    return render(request, 'post.html', context)


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        title = Post.objects.filter(title__icontains=query)
        description = Post.objects.filter(description__icontains=query)
        posts = title | description
        context = {'posts': posts, 'title': f'Search for {query}'}
        return render(request, 'search.html', context)
    else:
        return redirect('/')

# ------------------------ Page Views ----------------------

def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page/page.html', {'page': page, "title": page.title})


def pages(request):
    pages = Page.objects.all().order_by('created')
    return render(request, 'page/list.html', {'pages': pages, "title": "Pages"})

def createPage(request):
    form = FormCreatePage()
    if request.method == 'POST' and request.user.is_superuser:
        form = FormCreatePage(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages')
    context = {"form": form}
    return render(request, 'page/create.html', context)


def updatePage(request, id):
    page = Page.objects.get(id=id)
    form = FormCreatePage(instance=page)
    if request.method == 'POST' and request.user.is_superuser:
        form = FormCreatePage(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('pages')
    context = {"form": form}
    return render(request, 'page/update.html', context)

def deletePage(request, id):
    page = Page.objects.get(id=id)
    if request.user.is_superuser:
        operation = page.delete()
        if operation:
            messages.success(request, 'Page deleted successfully.')
            return redirect('pages')

        else:
            messages.warning(request, 'Page deleted failde ')
            return redirect('pages')

    return redirect('home')


def lable(request, lable):
    posts = Post.objects.filter(title__icontains=lable)
    context = {"posts": posts, 'title': f"{lable} - PoolsBox"}
    return render(request, 'lable.html', context)

def menu(request):
    context = {'title': 'Menu - PoolsBox'}
    return render(request, 'menu.html', context)


def contact(request):
    form = CreateContact()
    if request.method == "POST":
        form = CreateContact(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The message has been sent successfully')
            return redirect('contact')
    context = {'form':form,'title':'PoolsBox - Contace'}
    return render(request, 'contact/contact.html', context)




































def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    soup2 = soup.find("div", class_='entry-content')
    try:
        divs = len(soup2.find_all('div'))
        scripts = len(soup2.find_all('script'))
        noscripts = len(soup2.find_all('noscript'))
        centers = len(soup2.find_all('center'))
        list = [divs, scripts, noscripts, centers]
    except:
        list = [50, 40]
    for item in range(0, max(list)):
        if soup2.find('div'):
            soup2.find('div').decompose()
        if soup.find('center'):
            soup2.find('center').decompose()
        if soup2.find('script'):
            soup2.find('script').decompose()
        if soup2.find('noscript'):
            soup2.find('noscript').decompose()
        try:
            tag = soup2.html.body
        except:
            try:
                tag = soup2.html
            except:
                tag = soup2
    return tag


def scraping(request):
    for page in range(1, 77):
        url = f"https://www.nomadicmatt.com/travel-blog/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("article")

        for item in results:

            title = item.find("h2").find('a').text
            try:
                image = item.find('img')['data-lazy-src']
            except:
                image = ''
            link = item.find("h2").find('a')['href']

            # Post detail scraping
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(title=str(title), image_link=str(image), body=str(getItem(link)).replace('<body', '<article'))
                print("not exists...")
            print(link)
    return JsonResponse({'message': 'Scraping successfully...'})
