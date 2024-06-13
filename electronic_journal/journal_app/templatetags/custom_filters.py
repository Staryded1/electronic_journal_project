from django import template
from ..models import JournalEntry

register = template.Library()

@register.filter(name='to')
def to(start, end):
    return range(start, end + 1)



@register.filter
def get_student_mark(lesson, student_day):
    student, day = student_day
    try:
        entry = JournalEntry.objects.get(lesson=lesson, student=student, day=day)
        return entry.mark
    except JournalEntry.DoesNotExist:
        return ''