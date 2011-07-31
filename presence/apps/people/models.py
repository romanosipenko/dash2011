from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse

import datetime

from workflow.models import StateLog


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"))
    start_work = models.DateField(_("Start work"),
        help_text=_("Define when user start working with team."))
    vacation_days = models.PositiveIntegerField(_("Vacation days"),
        help_text=_("Vacation days for user per year."),
        default=24)
    vacation_days_used = models.PositiveIntegerField(
        _("User vacation days"),
        help_text=_("Already used vacation days this year."),
        default=0
        )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = ("Profiles")
        ordering = ("-updated",)

    def __unicode__(self):
        return self.user.get_full_name() if \
            self.user.get_full_name() else \
            self.user.username

    @property
    def state(self):
        if not hasattr(self, '_state_log'):
            self._state_log = StateLog.objects.get_user_current_state_log(
                self.user
            )
        return self._state_log.state

    @property
    def location(self):
        if not hasattr(self, '_state_log'):
            self._state_log = StateLog.objects.get_user_current_state_log(
                self.user
            )
        return self._state_log.location

    @property
    def project(self):
        if not hasattr(self, '_state_log'):
            self._state_log = StateLog.objects.get_user_current_state_log(
                self.user
            )
        return self._state_log.project


def create_profile(sender, **kwargs):
    """Create profile for newely created user"""
    if kwargs['created']:
        user = kwargs['instance']
        profile = Profile(user=user)
        profile.start_work = datetime.date.today()
        user.is_active = False
        user.save()
        profile.save()

        # Generate email with activation/autologin code
        from activation.models import ActivationKey
        _key = ActivationKey.objects.create_key(user)
        link = reverse("activate-user", args=[_key.key])
        send_mail(
            '[Presence]',
            'Be quiet! You have one shot! \n Here is approve link %s' % link,
            settings.DEFAULT_FROM_EMAIL,
            [user.email], fail_silently=False
            )

post_save.connect(create_profile, sender=User,\
    dispatch_uid="create.profile.after.user")
