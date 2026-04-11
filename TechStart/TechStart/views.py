from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import re
from learning.models import LearningPath, Module, Topic, UserProgress, ChatMessage
from learning.utils import get_ai_tutor_response
from learning.models import LearningPath, Module, Topic, UserProgress, ChatMessage


def home_view(request):
    return render(request, 'home.html')

# @login_required
# def learning_options_view(request):
#     # FETCH DB DATA: Get all modules (Computer Basics, Excel, etc.)
#     modules = Module.objects.all().order_by('path', 'name')
#     return render(request, 'learning_options.html', {'modules': modules})

# @login_required
# def topic_selection_view(request, module_slug):
#     # FETCH DB DATA: Get the specific module by its slug
#     module = get_object_or_404(Module, slug=module_slug)
    
#     # Find the first topic to start the lesson
#     first_topic = module.topics.first()
    
#     context = {
#         'title': module.name,
#         'description': module.description,
#         'first_topic': first_topic,
#         'topics_count': module.topics.count()
#     }
#     return render(request, 'topic_selection.html', context)

@login_required
def chat_view(request, topic_id=None):
    topic = None
    chat_history = []
    toc_topics = []
    
    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id)
        request.session['current_topic_name'] = topic.name
        request.session['current_topic_id'] = topic.id
        
        chat_history = ChatMessage.objects.filter(user=request.user, topic=topic)
        
        # CHANGED: Filter topics by MODULE, not Path
        toc_topics = Topic.objects.filter(module=topic.module).order_by('order')

    else:
        # --- NEW: SANDBOX / TRIAL MODE ---
        # User clicked "Try AI Chatbot" on the home page.
        # 1. Clear the previous topic memory so it doesn't bleed over!
        request.session['current_topic_name'] = "Computer Basics and Programming"
        request.session.pop('current_topic_id', None) # Safely removes the old ID
        
        # 2. Fetch "Global" chat history (where topic is completely empty)
        chat_history = ChatMessage.objects.filter(user=request.user, topic__isnull=True)


    completed_ids = UserProgress.objects.filter(user=request.user, completed=True).values_list('topic_id', flat=True)
    
    context = {
        'current_topic': topic,
        'chat_history': chat_history,
        'toc_topics': toc_topics,
        'completed_ids': completed_ids,
    }
    return render(request, 'chat_interface.html', context)

@login_required
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '').strip()
            
            topic_name = request.session.get('current_topic_name', 'General')
            topic_id = request.session.get('current_topic_id')
            current_state = request.session.get('chat_state', 'teach') 
            quiz_context = request.session.get('quiz_context', '')
            
            # Get User Learning History
            completed_names = UserProgress.objects.filter(
                user=request.user, 
                completed=True
            ).values_list('topic__name', flat=True)
            
            history_string = ""
            if completed_names:
                history_string = f"User has already mastered: {', '.join(completed_names)}."

            topic_obj = None
            if topic_id:
                topic_obj = Topic.objects.get(id=topic_id)

            # Save User Message
            ChatMessage.objects.create(
                user=request.user, 
                topic=topic_obj, 
                sender='user', 
                message=user_input
            )

            # # --- NEW: GREETING INTERCEPTOR ---
            # # If the user just says a simple hello, respond instantly without calling the AI model.
            # clean_input = re.sub(r'[^\w\s]', '', user_input.lower()).strip() # removes punctuation
            # greetings = ['hi', 'hello', 'hey', 'hi there', 'hello there', 'namaste' , 'how are you']
            
            # if clean_input in greetings and current_state != 'awaiting_answer':
            #     greeting_response = f"Hello! 👋 I am your AI Tutor. Let's learn about **{topic_name}**. You can ask me any question, or just say 'Teach me' to begin!"
                
            #     # Save AI Response to DB
            #     ChatMessage.objects.create(
            #         user=request.user, 
            #         topic=topic_obj, 
            #         sender='ai', 
            #         message=greeting_response,
            #         is_quiz=False
            #     )
            #     return JsonResponse({'response': greeting_response})
            # # --- END GREETING INTERCEPTOR ---

            # api_mode = "teach"
            # if "quiz" in user_input.lower() or "test" in user_input.lower() or "क्विज़" in user_input:
            #     api_mode = "quiz"
            #     request.session['chat_state'] = 'awaiting_answer' 
            # elif current_state == 'awaiting_answer':
            #     api_mode = "grade"
            #     request.session['chat_state'] = 'teach' 
            # else:
            #     api_mode = "teach"

            # 4. Determine Mode (State Machine)
            api_mode = "teach"
            
            # Clean the input to check for exact greetings (removes punctuation)
            clean_input = re.sub(r'[^\w\s]', '', user_input.lower()).strip()
            greetings = ['hi', 'hello', 'hey', 'hi there', 'hello there', 'namaste', 'नमस्कार']

            if "quiz" in user_input.lower() or "test" in user_input.lower() or "क्विज़" in user_input:
                api_mode = "quiz"
                request.session['chat_state'] = 'awaiting_answer' 
            elif current_state == 'awaiting_answer':
                api_mode = "grade"
                request.session['chat_state'] = 'teach' 
            elif clean_input in greetings:
                # NEW: Route greetings to the "chat" mode we added to main.py
                api_mode = "chat"
            else:
                api_mode = "teach"

            language = 'English'
            try:
                language = request.user.profile.preferred_language
            except:
                pass
            
            full_context = f"{quiz_context} {history_string}".strip()
            
            ai_response_text = get_ai_tutor_response(
                mode=api_mode,
                topic=topic_name,
                language=language,
                user_input=user_input,
                context=full_context
            )
            
            if api_mode == "quiz":
                request.session['quiz_context'] = ai_response_text
                pattern = r'(Correct\s*Answer|Answer|Correct\s*Option|उत्तर)\s*[:\-\)].*'
                match = re.search(pattern, ai_response_text, re.IGNORECASE | re.DOTALL)
                if match:
                    ai_response_text = ai_response_text[:match.start()].strip()

            if api_mode == "grade" and topic_id:
                text_lower = ai_response_text.lower()
                is_correct = ("correct" in text_lower or "right" in text_lower or "सही" in ai_response_text)
                is_negated = ("not correct" in text_lower or "incorrect" in text_lower)

                if is_correct and not is_negated:
                    try:
                        UserProgress.objects.update_or_create(
                            user=request.user,
                            topic=topic_obj,
                            defaults={'completed': True, 'quiz_score': 100}
                        )
                    except:
                        pass
                request.session['quiz_context'] = ""

            ChatMessage.objects.create(
                user=request.user, 
                topic=topic_obj, 
                sender='ai', 
                message=ai_response_text,
                is_quiz=(api_mode == "quiz")
            )

            return JsonResponse({'response': ai_response_text})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def set_language_view(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang in ['English', 'Hindi', 'Marathi']:
            profile = request.user.profile
            profile.preferred_language = lang
            profile.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def path_selection_view(request):
    """
    Step 1: Display Main Learning Paths (e.g., Computer Skills, Programming)
    """
    paths = LearningPath.objects.all()
    return render(request, 'path_selection.html', {'paths': paths})

@login_required
def module_selection_view(request, path_slug):
    """
    Step 2: Display Modules for the selected Path
    """
    learning_path = get_object_or_404(LearningPath, slug=path_slug)
    modules = Module.objects.filter(path=learning_path).order_by('name')
    
    context = {
        'learning_path': learning_path,
        'modules': modules
    }
    return render(request, 'module_selection.html', context)

# ... topic_selection_view remains the same (Step 3) ...
@login_required
def topic_selection_view(request, module_slug):
    # FETCH DB DATA: Get the specific module by its slug
    module = get_object_or_404(Module, slug=module_slug)
    
    # Find the first topic to start the lesson
    first_topic = module.topics.first()
    
    context = {
        'title': module.name,
        'description': module.description,
        'first_topic': first_topic,
        'topics_count': module.topics.count()
    }
    return render(request, 'topic_selection.html', context)


def about_view(request):
    """Renders the About page."""
    return render(request, 'about.html')