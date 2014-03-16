from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request):
    ## not needed at this time... chapter 6
    # if request.method == 'POST':
    #     Item.objects.create(text = request.POST['item_text'])
    #     return  redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list= list_, data=request.POST)
        if form.is_valid():
            #Item.objects.create(text = request.POST['text'], list = list_)
            form.save()
            # return  redirect('/lists/%d/' % (list_.id,)) hard-coded URL
            return redirect(list_) # using get_absolute_url to redirect
    return render(request, 'list.html', {'list': list_, "form": form })

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        #Item.objects.create(text = request.POST['text'], list = list_)
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
    # return redirect(list_) # using get_absolute_url in Lists.models.py
    # return  redirect('/lists/%d/' % (list_.id,)) - how we started with hard-coded URL
    # return redirect('view_list', lisd_.id) as an alternative to above hard coded URL

# Changed this to the view_list function:
# def add_item(request, list_id):
#     list_ = List.objects.get(id = list_id)
#     Item.objects.create(text = request.POST['item_text'], list = list_)
#     return  redirect('/lists/%d/' % (list_.id,))

def my_lists(request, email):
    return render(request, 'my_lists.html')