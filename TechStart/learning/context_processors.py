from .translations import CONTENT

def language_content(request):
    """
    Injects the translation dictionary into the template context
    based on the logged-in user's preference.
    """
    # Default language
    lang = 'English' 
    
    if request.user.is_authenticated:
        try:
            # Try to get from profile
            lang = request.user.profile.preferred_language
        except:
            pass
            
    # Return the dictionary matching the language, or fallback to English
    return {'text': CONTENT.get(lang, CONTENT['English'])}