from django.contrib import admin
from .models import Exam,ExamAns,Tests,registers
# Register your models here.
admin.site.register(Tests)
admin.site.register(Exam)
admin.site.register(ExamAns)
admin.site.register(registers)
