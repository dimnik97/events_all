from django.db import models
from django.views.decorators.csrf import csrf_exempt


from custom_profile.models import Profile
from django.db.models.signals import post_save


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)
    creator_id = models.ForeignKey(Profile, on_delete = models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    participants = models.IntegerField(null=True,blank=True)

    def get_events():
        events = Event.objects.all()
        return events

    def __str__(self):
        return self.name + ' Создатель: ' + self.creator_id.user.first_name




class EventParty(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete = models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'event_id',)

    @csrf_exempt
    def subscribe_event(request):
        # функция подписки на событие
        new_subscriber = EventParty()
        new_subscriber.event_id = Event.objects.get(id=int(request.POST['event_id']))
        new_subscriber.user_id = Profile.objects.get(id=request.user.id)
        new_subscriber.save()
        pass

    def __str__(self):
        return self.user_id.user.first_name + " Участник: " + self.event_id.name




def event_creating_post_save(sender, instance, created, **kwargs):
    if created:
        event_join = EventParty()
        event_join.user_id = instance.creator_id
        event_join.event_id = instance
        event_join.save()
post_save.connect(event_creating_post_save, sender=Event)