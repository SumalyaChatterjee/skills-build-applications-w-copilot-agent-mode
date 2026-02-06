from rest_framework import serializers
from django.contrib.auth.models import User
from .models import HSFitKid, Grp, Drl, Pln


class USerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class KSerial(serializers.ModelSerializer):
    u = USerial(read_only=True)
    un = serializers.CharField(write_only=True, required=False)
    hid = serializers.SerializerMethodField()
    
    class Meta:
        model = HSFitKid
        fields = ['id', 'u', 'un', 'gr', 'tgt', 'pts', 'str_k', 'bdg', 'mul', 'hid', 'ts']
        read_only_fields = ['pts', 'ts']
    
    def get_hid(self, obj):
        return obj.h_tag()
    
    def create(self, validated_data):
        un = validated_data.pop('un', None)
        if un:
            u, _ = User.objects.get_or_create(username=un)
            validated_data['u'] = u
        return super().create(validated_data)


class GSerial(serializers.ModelSerializer):
    ldr = KSerial(read_only=True)
    lid = serializers.IntegerField(write_only=True, required=False)
    mbs = KSerial(many=True, read_only=True)
    mids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    mc = serializers.SerializerMethodField()
    pw = serializers.SerializerMethodField()
    
    class Meta:
        model = Grp
        fields = ['id', 'nm', 'slog', 'ldr', 'lid', 'mbs', 'mids', 'mc', 'pts', 'ws', 'col', 'pw', 'ts']
        read_only_fields = ['pts', 'ts']
    
    def get_mc(self, obj):
        return obj.mbs.count()
    
    def get_pw(self, obj):
        return obj.pts_calc()
    
    def create(self, validated_data):
        mids = validated_data.pop('mids', [])
        lid = validated_data.pop('lid', None)
        
        if lid:
            validated_data['ldr_id'] = lid
        
        g = super().create(validated_data)
        
        if mids:
            g.mbs.set(mids)
        
        return g


class DSerial(serializers.ModelSerializer):
    k = KSerial(read_only=True)
    kid = serializers.IntegerField(write_only=True)
    dh = serializers.SerializerMethodField()
    
    class Meta:
        model = Drl
        fields = ['id', 'k', 'kid', 'knd', 'tm', 'eff', 'pts', 'nt', 'wx', 'dh', 'ts']
        read_only_fields = ['pts', 'ts']
    
    def get_dh(self, obj):
        h = sum(ord(c) for c in f"{obj.id}{obj.knd}{obj.tm}")
        return f"D{h % 999999:06d}"
    
    def create(self, validated_data):
        d = super().create(validated_data)
        d.pts_calc()
        d.save()
        d.k.pts_calc()
        return d


class PSerial(serializers.ModelSerializer):
    ps = serializers.SerializerMethodField()
    
    class Meta:
        model = Pln
        fields = ['id', 'nm', 'hw', 'tr', 'mn', 'fz', 'gr', 'lks', 'ps', 'ts']
        read_only_fields = ['ts', 'lks']
    
    def get_ps(self, obj):
        if obj.lks > 60:
            return 'hot'
        elif obj.lks > 25:
            return 'warm'
        else:
            return 'new'


class RSerial(serializers.Serializer):
    p = serializers.IntegerField()
    n = serializers.CharField()
    pt = serializers.IntegerField()
    s = serializers.IntegerField()
    g = serializers.CharField()
    m = serializers.FloatField()

