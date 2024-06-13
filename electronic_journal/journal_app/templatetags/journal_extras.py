from django import template
from journal_app.models import JournalEntry

register = template.Library()

@register.filter(name='is_lesson_day')
def is_lesson_day(day, lessons):
    return any(lesson.date.day == day for lesson in lessons)

@register.filter(name='get_student_mark')
def get_student_mark(entries, args):
    if isinstance(args, str):
        student, day = map(int, args.split(','))
    elif isinstance(args, (list, tuple)) and len(args) == 2:
        student, day = args
    else:
        return ''

    entry = entries.filter(student_id=student, day=day).first()
    return entry.mark if entry else ''

@register.simple_tag
def get_entry(journal_entries, student_id, day):
    student_id = int(student_id)
    day = int(day)
    entry = journal_entries.filter(student_id=student_id, day=day).first()
    return entry.mark if entry else ''