from django.contrib import admin
from .models import AnswerSheet, Answer


class SheetAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'contestant', 'start_time', 'end_time', 'is_attempted', 'is_graded', 'total_marks_obtained')
    list_filter = ('quiz', 'is_valid', 'is_attempted', 'is_graded')
    fieldsets = (
        (None, {'fields': ('quiz', 'contestant')}),
        ('Marks info', {'fields': ('total_marks_available', 'total_marks_obtained', 'total_subjective_marks', 'total_objective_positive',
                                   'total_objective_negative')}),
        ('Time Tracker', {'fields': ('start_time', 'end_time', 'current_time')}),
        ('Flags', {'fields': ('is_valid', 'is_attempted', 'is_graded')}),
    )
    ordering = ('quiz', 'contestant', 'start_time', 'end_time', 'is_valid', 'total_marks_obtained')
    filter_horizontal = ()


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('sheet', 'question', 'marks_awarded', 'is_attempted', 'is_graded')
    list_filter = ('sheet', 'is_attempted', 'is_graded')
    fieldsets = (
        (None, {'fields': ('sheet', 'question', 'marks_awarded', 'is_attempted', 'is_graded')}),
        ('Time', {'fields': ('response_time',)}),
        ('If Subjective', {'fields': ('subjective_answer', )}),
        ('If Objective', {'fields': ('response_A', 'response_B', 'response_C', 'response_D')}),
    )
    ordering = ('sheet', 'question', 'marks_awarded', 'is_attempted')
    filter_horizontal = ()


admin.site.register(AnswerSheet, SheetAdmin)
admin.site.register(Answer, AnswerAdmin)
