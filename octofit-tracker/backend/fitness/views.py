from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import HSFitKid, Grp, Drl, Pln
from .serializers import KSerial, GSerial, DSerial, PSerial, RSerial


@api_view(['GET'])
def hub(request):
    return Response({
        's': 'OctoFit',
        'v': '5.2',
        'r': {
            'k': '/hub/k/',
            'g': '/hub/g/',
            'd': '/hub/d/',
            'p': '/hub/p/',
            'rank': '/hub/rank/',
            'bat': '/hub/bat/',
        }
    })


class KVS(viewsets.ModelViewSet):
    queryset = HSFitKid.objects.all()
    serializer_class = KSerial
    
    @action(detail=True, methods=['get'])
    def df(self, request, pk=None):
        k = self.get_object()
        ds = k.drls.all()[:35]
        s = DSerial(ds, many=True)
        
        tm = sum(d.tm for d in ds)
        ae = sum(d.eff for d in ds) / len(ds) if ds else 0
        
        return Response({
            'd': s.data,
            'm': {
                'c': len(ds),
                't': tm,
                'a': round(ae, 1)
            }
        })
    
    @action(detail=True, methods=['post'])
    def bst(self, request, pk=None):
        k = self.get_object()
        a = request.data.get('a', 0.15)
        k.mul += float(a)
        k.pts_calc()
        
        return Response({
            'm': k.mul,
            'p': k.pts
        })
    
    @action(detail=False, methods=['get'])
    def top_s(self, request):
        ts = self.queryset.filter(str_k__gt=0).order_by('-str_k')[:12]
        s = self.get_serializer(ts, many=True)
        return Response(s.data)


class GVS(viewsets.ModelViewSet):
    queryset = Grp.objects.all()
    serializer_class = GSerial
    
    @action(detail=True, methods=['post'])
    def add_m(self, request, pk=None):
        g = self.get_object()
        kid = request.data.get('kid')
        
        try:
            k = HSFitKid.objects.get(id=kid)
            g.mbs.add(k)
            np = g.pts_calc()
            
            return Response({
                'ok': 1,
                'p': np,
                's': g.mbs.count()
            })
        except HSFitKid.DoesNotExist:
            return Response({'e': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def top_p(self, request):
        gs = self.queryset.all()
        for g in gs:
            g.pts_calc()
        
        ts = Grp.objects.order_by('-pts')[:15]
        s = self.get_serializer(ts, many=True)
        return Response(s.data)
    
    @action(detail=True, methods=['post'])
    def win(self, request, pk=None):
        g = self.get_object()
        g.ws += 1
        g.pts_calc()
        
        return Response({
            'w': g.ws,
            'p': g.pts
        })


class DVS(viewsets.ModelViewSet):
    queryset = Drl.objects.all()
    serializer_class = DSerial
    
    def perform_create(self, s):
        d = s.save()
        d.pts_calc()
        d.save()
        d.k.pts_calc()
    
    @action(detail=False, methods=['get'])
    def hot(self, request):
        h = self.queryset.filter(eff__gte=8).order_by('-ts')[:25]
        s = self.get_serializer(h, many=True)
        return Response(s.data)
    
    @action(detail=False, methods=['get'])
    def knd(self, request):
        k = request.query_params.get('k', 'rn')
        f = self.queryset.filter(knd=k)[:18]
        s = self.get_serializer(f, many=True)
        return Response(s.data)


class PVS(viewsets.ModelViewSet):
    queryset = Pln.objects.all()
    serializer_class = PSerial
    
    @action(detail=False, methods=['get'])
    def tr(self, request):
        t = request.query_params.get('t', 'g')
        ps = self.queryset.filter(tr=t)
        s = self.get_serializer(ps, many=True)
        return Response(s.data)
    
    @action(detail=False, methods=['get'])
    def qk(self, request):
        q = self.queryset.filter(mn__lte=30).order_by('mn')
        s = self.get_serializer(q, many=True)
        return Response(s.data)
    
    @action(detail=True, methods=['post'])
    def lk(self, request, pk=None):
        p = self.get_object()
        p.lk_up()
        s = self.get_serializer(p)
        return Response(s.data)


@api_view(['GET'])
def rank(request):
    ks = HSFitKid.objects.order_by('-pts', '-str_k')[:25]
    
    d = [
        {
            'p': i + 1,
            'n': k.u.username,
            'pt': k.pts,
            's': k.str_k,
            'g': k.gr,
            'm': k.mul
        }
        for i, k in enumerate(ks)
    ]
    
    s = RSerial(d, many=True)
    return Response(s.data)


@api_view(['GET'])
def bat(request):
    gs = Grp.objects.all()
    
    for g in gs:
        g.pts_calc()
    
    ts = Grp.objects.order_by('-pts')[:12]
    
    d = [
        {
            'r': i + 1,
            'n': g.nm,
            'p': g.pts,
            's': g.mbs.count(),
            'w': g.ws,
            'c': g.col
        }
        for i, g in enumerate(ts)
    ]
    
    return Response({'res': d})

