from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from custom_profile.models import Profile
from django.db.models.signals import post_save


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)
    creator_id = models.ForeignKey(User, on_delete = models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    participants = models.IntegerField(null=True,blank=True)

    def get_events():
        events = Event.objects.all()
        return events

    def __str__(self):
        return self.name + ' Создатель: ' + self.creator_id.first_name




class EventParty(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(User)
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)

    @classmethod
    def subscr_to_event(cls, ev_id, u_id):
        eventparty, created = cls.objects.get_or_create(
            event_id=ev_id
        )
        eventparty.user_id.add(u_id)

    @classmethod
    def unsubscr_from_event(cls, ev_id, u_id):
        eventparty, created = cls.objects.get_or_create(
            current_user=ev_id
        )
        eventparty.user_id.remove(u_id)


    @csrf_exempt
    def subscribe_event(request):
        # функция подписки/отписки на событие
        if request.is_ajax():
            try:
                # subscriber = EventParty()
                event_id = Event.objects.get(id=int(request.POST['event_id']))
                subscriber.event_id = event_id
                subscriber.user_id = User.objects.get(id=request.user.id)

                if (request.POST['action'] == "subscribe"):

                    EventParty.unsubscr_from_event()

                elif (request.POST['action'] == "unsubscribe"):

                    subscriber.delete()

            except KeyError:
                return HttpResponse('Error')

        return HttpResponse(str(200))

    # def __str__(self):
    #     return self.user_id.first_name + " Участник: " + self.event_id.name




def event_creating_post_save(sender, instance, created, **kwargs):
    if created:
        event_join = EventParty()
        event_join.user_id = instance.creator_id
        event_join.event_id = instance
        event_join.save()
post_save.connect(event_creating_post_save, sender=Event)