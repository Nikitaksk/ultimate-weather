from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import reportIssueForm
from django.conf import settings
from django.core.mail import send_mail

@login_required(login_url="/users/login/")
def report(request):
    if request.method == "GET":
        form = reportIssueForm()
        return render(request, "notifications/report.html", {'form': form})
    else:
        form = reportIssueForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            my_mail = [settings.my_email,]
            subject = 'Thank you for your feedback at Beautiful Weather'
            message = (f"Hi, {form.cleaned_data['name']}, thank you giving feedback on my app. I've received the email "
                       f"too and will do my best dealing with your issues\n Mikita Kasiak")
            email_from = settings.EMAIL_HOST_USER

            recipient_list = [form.cleaned_data['email']]
            print(subject, message, email_from, recipient_list)
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            subject = "New bug report in weather!"
            message = f'From: {form.cleaned_data['name']} (username: {request.user}). \n' + f'Category: {form.cleaned_data['issue_type']} \n' + f'Description: {form.cleaned_data['issue_desc']} \n'
            send_mail(subject, message, email_from, my_mail, fail_silently=False)
            return render(request, "notifications/report.html", {'message': 'Thank you!'})
        else:
            return render(request, "notifications/report.html", {'form': form})
