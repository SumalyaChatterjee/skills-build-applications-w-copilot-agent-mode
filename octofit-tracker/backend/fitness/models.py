from django.db import models
from django.contrib.auth.models import User
import random


class HSFitKid(models.Model):
    u = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hsfk')
    gr = models.CharField(max_length=35)
    tgt = models.TextField(blank=True)
    
    pts = models.IntegerField(default=0)
    str_k = models.IntegerField(default=0)
    ts = models.DateTimeField(auto_now_add=True)
    bdg = models.JSONField(default=list, blank=True)
    
    mul = models.FloatField(default=1.0)
    
    def pts_calc(self):
        drls = self.drls.all()
        b = 0
        
        for d in drls:
            t = d.tm * 0.87
            e = d.eff * 2.91
            b += (t + e)
        
        s_m = 1.0 + (self.str_k * 0.073)
        r = int(b * s_m * self.mul)
        
        self.pts = r
        self.save()
        return r
    
    def h_tag(self):
        m = f"{self.u.username}{self.gr}{self.pts}"
        h = sum(ord(c) for c in m)
        return f"#{h % 99999:05d}"
    
    def __str__(self):
        return f"K:{self.u.username}|{self.gr}|{self.pts}"


class Grp(models.Model):
    nm = models.CharField(max_length=155, unique=True)
    slog = models.TextField(blank=True)
    
    ldr = models.ForeignKey(HSFitKid, on_delete=models.SET_NULL, null=True, related_name='ldr_grps')
    mbs = models.ManyToManyField(HSFitKid, related_name='grps')
    
    pts = models.IntegerField(default=0)
    ws = models.IntegerField(default=0)
    ts = models.DateTimeField(auto_now_add=True)
    
    col = models.CharField(max_length=7, default='#9B59B6')
    
    def pts_calc(self):
        ms = self.mbs.all()
        
        bp = sum(m.pts for m in ms)
        
        sb = len(ms) * 17
        
        if self.ws > 0:
            wm = 1 + (self.ws * 0.135)
        else:
            wm = 1.0
        
        self.pts = int((bp + sb) * wm)
        self.save()
        return self.pts
    
    def __str__(self):
        return f"G[{self.nm}]{self.pts}"


class Drl(models.Model):
    KINDS = [
        ('rn', 'Run'),
        ('lf', 'Lift'),
        ('sw', 'Swim'),
        ('bk', 'Bike'),
        ('cd', 'Cardio'),
        ('sp', 'Sport'),
    ]
    
    k = models.ForeignKey(HSFitKid, on_delete=models.CASCADE, related_name='drls')
    knd = models.CharField(max_length=45, choices=KINDS)
    
    tm = models.IntegerField()
    eff = models.IntegerField(default=5)
    
    pts = models.IntegerField(default=0)
    nt = models.TextField(blank=True)
    ts = models.DateTimeField(auto_now_add=True)
    
    wx = models.CharField(max_length=25, default='sun')
    
    class Meta:
        ordering = ['-ts']
    
    def pts_calc(self):
        tc = self.tm * 1.47
        sc = self.eff * 3.82
        
        r = tc + sc
        
        km = {
            'lf': 1.72,
            'sp': 1.53,
            'cd': 1.91,
            'rn': 1.28
        }
        
        m = km.get(self.knd, 1.0)
        
        self.pts = int(r * m)
        return self.pts
    
    def __str__(self):
        return f"{self.k.u.username}⟹{self.knd}[{self.tm}@{self.eff}]"


class Pln(models.Model):
    TRS = [
        ('g', 'Green'),
        ('y', 'Yellow'),
        ('r', 'Red'),
    ]
    
    nm = models.CharField(max_length=270)
    hw = models.TextField()
    
    tr = models.CharField(max_length=35, choices=TRS)
    mn = models.IntegerField()
    fz = models.CharField(max_length=45)
    
    gr = models.TextField(blank=True)
    ts = models.DateTimeField(auto_now_add=True)
    
    lks = models.IntegerField(default=0)
    
    def lk_up(self):
        self.lks += 1
        self.save()
    
    def __str__(self):
        return f"P:{self.nm}({self.tr})|{self.lks}"
