from django.shortcuts import render
from django.http import HttpResponse
from .functions import extract_text_from_pdf, generate_analysis
import os
from pathlib import Path
import json
from .models import History
from datetime import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
def home(request):    
    context = {"loggedin": "false"}
    
    if request.user.is_authenticated:
        context.update({
            "loggedin": "true",
            # "name": request.user.first_name,
            "username": request.user.username
        })
    print(context)    
    return render(request, 'landing.html', context)


# Create your views here.
def dashboard(request):       
    if request.method == 'POST':
        uploaded_file = request.FILES.get('pdf')  # Access the file from POST data
        if not uploaded_file:
            return HttpResponse("No PDF uploaded", status=400)

        # Define the directory path
        temp_dir = os.path.join(BASE_DIR, "temp")

        # Ensure the directory exists
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Save the uploaded file temporarily
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        
        # Extract text from the PDF
        file_content = extract_text_from_pdf(temp_path)

        # Clean up the temporary file
        os.remove(temp_path)

        if not file_content:
            return HttpResponse("Could not extract text from the PDF.", status=500)

        # Truncate the content to avoid token limits
        if len(file_content) > 50000:
            file_content = file_content[:50000]

        # Generate analysis
        analysis_result = generate_analysis(file_content)

        # Save the analysis result to a file (optional)
        output_file = 'pdf_analysis_output.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis_result)
        analysis_result = json.loads(analysis_result)

                # Save history to the database
        History.objects.create(
            username=request.user.username,  # Assuming user is authenticated
            filename=uploaded_file.name,
            date_created=datetime.now(),
            json_file=analysis_result
        )
        # Pass the result to the results template
        return render(request, 'results.html', {'analysis_result': analysis_result})
    return render(request, 'home.html')

from .models import History

def history_view(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        username = request.user.username  # Get the current user's username
        # Retrieve all history records for the current user
        history_items = History.objects.filter(username=username).order_by('-date_created')  # Latest first
        return render(request, 'history.html', {'history_items': history_items})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('login')
    
def results_view(request, history_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Retrieve the history entry based on the provided id
    history_item = get_object_or_404(History, id=history_id, username=request.user.username)
    
    # Get the JSON data from the history entry
    json_data = history_item.json_file

    # Pass the JSON data to the results.html template
    return render(request, 'results.html',  {'analysis_result': json_data})

def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})