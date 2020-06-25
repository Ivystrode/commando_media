from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages
from .models import Idea
from .forms import IdeaCreationForm, IdeaCommentForm, DeleteIdeaForm, EditIdeaForm


@login_required()
def ideas(request):
    if request.user.profile.approved:
        ideas = Idea.objects.all()


        context = {'user': request.user, 'ideas': ideas}


        return render(request, "ideas/ideas.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def idea_detail(request, id):
    if request.user.profile.approved:
        idea = Idea.objects.get(id=id)

        if request.method == "POST":
            form = IdeaCommentForm(request.POST)
            if form.is_valid():
                print("posting new comment")
                #create comment object but dont save to db yet
                new_comment = form.save(commit=False)
                print("comment picked up")
                #assign current article to the comment
                new_comment.parent = idea
                print("comment assigned to picture")
                new_comment.author = request.user
                #save comment to db
                new_comment.save()
                print("comment saved!")
                # return HttpResponseRedirect('') # clear form on submission
                return redirect(f'/ideas/{idea.id}')
        else:
            form = IdeaCommentForm()


        context = {'user': request.user, 'idea': idea, 'form':form}


        return render(request, "ideas/idea_detail.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def add_idea(request):  
    if request.user.profile.approved:
        if request.method == "POST":
            form = IdeaCreationForm(request.POST, request.FILES)
            if form.is_valid():
                new_idea = form.save(commit=False)
                print("save no commit")

                new_idea.created_by = request.user
                new_idea.slug = slugify(form.cleaned_data.get('title'))

                print(new_idea.created_by)
                print(form.cleaned_data)
                print(new_idea)

                new_idea.save()

                print("saved")

                ideaname = form.cleaned_data.get('title')
                print(form.cleaned_data)
                messages.success(request, f'idea created: {ideaname}')
                return redirect('/ideas')
        else:
            form = IdeaCreationForm()

        return render(request, "ideas/add_idea.html", {'form':form})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')


@login_required()
def delete_idea(request, id):
    if request.user.profile.approved:
        idea_to_delete = Idea.objects.get(id=id)
        context = {'idea':idea_to_delete}
        if request.method == "POST":
            if request.user == idea_to_delete.created_by or request.user.profile.staff:
                print("deleted" + str(idea_to_delete.title))
                idea_to_delete.delete()
                print("deleted")
                messages.success(request, f'Idea deleted')
                return redirect('/ideas')
            else:
                messages.success(request, f'You may only delete ideas if you are the creator or HQ staff')
                return redirect(f'/ideas')
        return render(request, "ideas/delete_idea.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def edit_idea(request, id):
    if request.user.profile.approved:
        print("EDIT ROUTE")
        idea = Idea.objects.get(id=id)
        if request.user == idea.created_by or request.user.profile.staff:
            if request.method == "POST":
                form = EditIdeaForm(request.POST, request.FILES, instance=idea)
                if form.is_valid():
                    edited_idea = form.save(commit=False)
                    print("form cleaned data")
                    print(form.cleaned_data)
                    print("edited idea")
                    edited_idea.created_by = idea.created_by
                    edited_idea.time = idea.time
                    edited_idea.slug = idea.slug
                    edited_idea.id = idea.id
                    print(edited_idea)
                    edited_idea.save()
                    messages.success(request, f'Edits saved to: {edited_idea.title}')
                    return redirect('/ideas')
            
            else:
                existing_data = {'title':idea.title, 'image': idea.image, 'body':idea.body}
                form = IdeaCreationForm(initial=existing_data)
        else:
            print("not staff user")
            messages.success(request, f'You may only edit this post if you are the creator or HQ staff')
            return render(request, "ideas/idea_detail.html", {'idea':idea})

        return render(request, "ideas/edit_idea.html", {'form':form, 'idea':idea})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

