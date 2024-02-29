from django.db import models
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    global PRIORITY
    class PRIORITY(models.IntegerChoices):
        URGENT = 1 #, _("Urgent")
        NORMAL = 2 #, _("Normal")
        LAZY = 3 #, _("Lazy")

    task = models.CharField(_('task title'), max_length=100, null=False, blank=False)
    description = models.CharField(_('task description'), max_length=255, null=True, default="None", blank=False)
    priority = models.PositiveIntegerField(_('task title'), choices=PRIORITY, default=PRIORITY.NORMAL)

    def get_priority_choices(self):
        return PRIORITY.choices

    def __str__(self) -> str:
        return f"({self.priority}) {self.task}"
    
    class Meta:
        """
        Meta options for the List model.
        """
        ordering = ['priority']
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    priority__in=[item for item in PRIORITY]
                    ), 
                name='cluster_priority_valid'
            ),
        ]