from django.shortcuts import render

# Data for the topics (would come from a database in a real app)
COMPUTER_TOPICS = [
    {'name': 'Microsoft Word', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>', 'color_class': 'bg-blue-500'},
    {'name': 'Microsoft Excel', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m3 6V7m-3 10h3M9 7h3m-3 4h3m-3 4h3m3-4h3m-3-4h3m-3-4h3M3 3h18v18H3V3z"></path>', 'color_class': 'bg-green-500'},
    {'name': 'PowerPoint', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12.016a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.498a4 4 0 01-8 0v-1.498m8 0h.01M6 12.016a4 4 0 108 0 4 4 0 00-8 0zm0 0v1.498a4 4 0 018 0v-1.498m-8 0H5.99M18 12.016a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.498a4 4 0 01-8 0v-1.498m8 0h.01M6 12.016a4 4 0 108 0 4 4 0 00-8 0zm0 0v1.498a4 4 0 018 0v-1.498m-8 0H5.99"></path>', 'color_class': 'bg-red-500'},
    {'name': 'Internet Basics', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9V3m0 18a9 9 0 009-9m-9 9a9 9 0 00-9-9"></path>', 'color_class': 'bg-yellow-500'},
]
PROGRAMMING_TOPICS = [
    {'name': 'Python', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>', 'color_class': 'bg-indigo-500'},
    {'name': 'Java', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"></path>', 'color_class': 'bg-pink-500'},
    {'name': 'C++', 'svg_path': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>', 'color_class': 'bg-purple-500'},
]

def home_view(request):
    return render(request, 'home.html')

def learning_options_view(request):
    return render(request, 'learning_options.html')

def topic_selection_view(request, path):
    context = {}
    if path == 'computer':
        context['title'] = 'Learn Computer Basics'
        context['topics'] = COMPUTER_TOPICS
    elif path == 'programming':
        context['title'] = 'Learn a Programming Language'
        context['topics'] = PROGRAMMING_TOPICS
    return render(request, 'topic_selection.html', context)

def chat_view(request):
    return render(request, 'chat_interface.html')

