from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages
from .models import Notice
from .forms import NoticeCreationForm, NoticeCommentForm, DeleteNoticeForm, EditNoticeForm

# Create your views here.
@login_required()
def home(request):


    context = {'user': request.user}
    print(request.user)


    return render(request, "main/home.html", context)

@login_required()
def notices(request):
    if request.user.profile.approved:
        notices = Notice.objects.all()


        context = {'user': request.user, 'notices': notices}


        return render(request, "main/notices.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def notice_detail(request, id):
    if request.user.profile.approved:
        notice = Notice.objects.get(id=id)

        if request.method == "POST":
            form = NoticeCommentForm(request.POST)
            if form.is_valid():
                print("posting new comment")
                #create comment object but dont save to db yet
                new_comment = form.save(commit=False)
                print("comment picked up")
                #assign current article to the comment
                new_comment.parent = notice
                print("comment assigned to picture")
                new_comment.author = request.user
                #save comment to db
                new_comment.save()
                print("comment saved!")
                # return HttpResponseRedirect('') # clear form on submission
                return redirect(f'/notices/{notice.id}')
        else:
            form = NoticeCommentForm()


        context = {'user': request.user, 'notice': notice, 'form':form}


        return render(request, "main/notice_detail.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def add_notice(request):
    if request.user.profile.approved:
        if request.user.profile.staff:    
            if request.method == "POST":
                form = NoticeCreationForm(request.POST, request.FILES)
                if form.is_valid():
                    new_notice = form.save(commit=False)
                    print("save no commit")

                    new_notice.created_by = request.user
                    new_notice.slug = slugify(form.cleaned_data.get('title'))

                    print(new_notice.created_by)
                    print(form.cleaned_data)
                    print(new_notice)

                    new_notice.save()

                    print("saved")

                    noticename = form.cleaned_data.get('title')
                    print(form.cleaned_data)
                    messages.success(request, f'Notice created: {noticename}')
                    return redirect('/notices')
            else:
                form = NoticeCreationForm()

            return render(request, "main/add_notice.html", {'form':form})
        else:
            messages.success(request, f'You must be in a HQ role to post notices')
            return redirect('/notices')
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')


@login_required()
def delete_notice(request, id):
    if request.user.profile.approved:
        notice_to_delete = Notice.objects.get(id=id)
        context = {'notice':notice_to_delete}
        if request.method == "POST":
            if request.user == notice_to_delete.created_by or request.user.profile.staff:
                print("deleted" + str(notice_to_delete.title))
                notice_to_delete.delete()
                print("deleted")
                messages.success(request, f'Notice deleted')
                return redirect('/notices')
            else:
                messages.success(request, f'You may only delete notices if you are the creator or HQ staff')
                return redirect(f'/notices')
        return render(request, "main/delete_notice.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def edit_notice(request, id):
    if request.user.profile.approved:
        print("EDIT ROUTE")
        notice = Notice.objects.get(id=id)
        if request.user == notice.created_by or request.user.profile.staff:
            if request.method == "POST":
                form = EditNoticeForm(request.POST, request.FILES, instance=notice)
                if form.is_valid():
                    edited_notice = form.save(commit=False)
                    print("form cleaned data")
                    print(form.cleaned_data)
                    print("edited notice")
                    edited_notice.created_by = notice.created_by
                    edited_notice.time = notice.time
                    edited_notice.slug = notice.slug
                    edited_notice.id = notice.id
                    print(edited_notice)
                    edited_notice.save()
                    messages.success(request, f'Edits saved to: {edited_notice.title}')
                    return redirect('/notices')
            
            else:
                existing_data = {'title':notice.title, 'image': notice.image, 'body':notice.body}
                form = NoticeCreationForm(initial=existing_data)
        else:
            print("not staff user")
            messages.success(request, f'You may only edit this post if you are the creator or HQ staff')
            return render(request, "main/notice_detail.html", {'notice':notice})

        return render(request, "main/edit_notice.html", {'form':form, 'notice':notice})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

