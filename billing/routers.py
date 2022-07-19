from rest_framework.routers import SimpleRouter
from .viewsets import BillViewSet


router = SimpleRouter()
router.register('bill', BillViewSet)
