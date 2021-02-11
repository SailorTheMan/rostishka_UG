from time import sleep

def start_countdown(User, pk, minutes):
    sleep(minutes * 60)
    user = User.objects.get(pk=pk)
    if not user.is_active:
        user.delete()
    