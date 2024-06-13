from django import template
from journal_app.models import JournalEntry

register = template.Library()

@register.filter(name='is_lesson_day')
def is_lesson_day(day, lessons):
    return any(lesson.date.day == day for lesson in lessons)

@register.simple_tag
def get_student_mark(entries, student_id, day):
    entry = entries.filter(student_id=student_id, day=day).first()
    return entry.mark if entry else ''
