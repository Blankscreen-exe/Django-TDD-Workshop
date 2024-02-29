from django import template

# REF: https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/
# REF: https://stackoverflow.com/questions/47792373/invalid-filter-error-in-django-custom-template-filter

register = template.Library()


@register.filter(name="get_priority_color")
def get_priority_color(value):
    """
    This filter takes a priority level and returns a corresponding background color.
    """
    colors = {
        1: '#f4a4a4',  # Most urgent
        2: '#ffe8d6',
        3: '#fbddff',
        # ... (add more levels with colors)
        # Default fallback color (optional)
        'default': 'lightgray'  # Least urgent
    }
    return colors.get(value, 'default')

register.filter('get_priority_color', get_priority_color)