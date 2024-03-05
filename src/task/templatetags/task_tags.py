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
        1: '#ff7171',  # Most urgent
        2: '#ffe8d6',
        3: '#b7b7b7',
        # ... (add more levels with colors)
        # Default fallback color (optional)
        'default': 'lightgray'  # Least urgent
    }
    return colors.get(value, 'default')

@register.filter(name="get_priority_star")
def get_priority_star(value):
    total_priorities=3
    start_count = total_priorities-value+1
    return start_count*"★" + ("(max)" if start_count==3 else "")

# you can also register filters like this 👇
# register.filter('get_priority_color', get_priority_color)
