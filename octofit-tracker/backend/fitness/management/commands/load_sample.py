from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fitness.models import HSFitKid, Grp, Drl, Pln

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        u1, _ = User.objects.get_or_create(username='alex_runner', defaults={'first_name': 'Alex', 'last_name': 'Thompson'})
        u2, _ = User.objects.get_or_create(username='sam_lifter', defaults={'first_name': 'Sam', 'last_name': 'Johnson'})
        u3, _ = User.objects.get_or_create(username='jess_swimmer', defaults={'first_name': 'Jess', 'last_name': 'Lee'})
        u4, _ = User.objects.get_or_create(username='mike_biker', defaults={'first_name': 'Mike', 'last_name': 'Chen'})
        
        k1, _ = HSFitKid.objects.get_or_create(u=u1, defaults={'gr': '10', 'tgt': 'Run 5K under 25 min', 'str_k': 5, 'mul': 1.2})
        k2, _ = HSFitKid.objects.get_or_create(u=u2, defaults={'gr': '11', 'tgt': 'Bench 200lbs', 'str_k': 3, 'mul': 1.1})
        k3, _ = HSFitKid.objects.get_or_create(u=u3, defaults={'gr': '10', 'tgt': 'Swim 1 mile', 'str_k': 7, 'mul': 1.3})
        k4, _ = HSFitKid.objects.get_or_create(u=u4, defaults={'gr': '12', 'tgt': '50 mile bike', 'str_k': 4, 'mul': 1.0})
        
        Drl.objects.get_or_create(k=k1, knd='rn', defaults={'tm': 45, 'eff': 8, 'nt': 'Morning run, felt great', 'wx': 'sunny'})
        Drl.objects.get_or_create(k=k1, knd='cd', defaults={'tm': 30, 'eff': 7, 'nt': 'HIIT session', 'wx': 'cloudy'})
        Drl.objects.get_or_create(k=k2, knd='lf', defaults={'tm': 60, 'eff': 9, 'nt': 'Chest day PR!', 'wx': 'indoor'})
        Drl.objects.get_or_create(k=k3, knd='sw', defaults={'tm': 50, 'eff': 8, 'nt': 'Lap swimming practice', 'wx': 'indoor'})
        Drl.objects.get_or_create(k=k4, knd='bk', defaults={'tm': 90, 'eff': 7, 'nt': 'Trail ride', 'wx': 'sunny'})
        
        g1, _ = Grp.objects.get_or_create(nm='Thunder Runners', defaults={'slog': 'Fast and Furious', 'ldr': k1, 'col': '#FF6B35'})
        g2, _ = Grp.objects.get_or_create(nm='Iron Squad', defaults={'slog': 'Lift Heavy', 'ldr': k2, 'col': '#4ECDC4'})
        
        g1.mbs.add(k1, k3)
        g2.mbs.add(k2, k4)
        
        Pln.objects.get_or_create(nm='Quick Morning Burst', defaults={
            'hw': '10 burpees, 20 jumping jacks, 15 pushups, repeat 3x',
            'tr': 'g', 'mn': 15, 'fz': 'Full body cardio', 'gr': 'None needed'
        })
        Pln.objects.get_or_create(nm='Strength Builder', defaults={
            'hw': 'Squats 3x10, Deadlifts 3x8, Bench 3x10, Rows 3x10',
            'tr': 'y', 'mn': 45, 'fz': 'Strength', 'gr': 'Barbell, weights'
        })
        Pln.objects.get_or_create(nm='Endurance Master', defaults={
            'hw': '5K run at steady pace, cooldown walk 10 min',
            'tr': 'r', 'mn': 40, 'fz': 'Cardio endurance', 'gr': 'Running shoes'
        })
        
        for k in [k1, k2, k3, k4]:
            k.pts_calc()
        
        for g in [g1, g2]:
            g.pts_calc()
        
        self.stdout.write('Sample data created!')
