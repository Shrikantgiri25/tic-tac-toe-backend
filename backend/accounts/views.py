# users/views.py
import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import User
from accounts.serializers.user_registeration_serializer import RegisterSerializer
from accounts.serializers.user_serializer import UserSerializer
from utils.custom_pagination import CustomPagination

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account with username, email, and password. Returns JWT tokens.",
        request=RegisterSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "user": UserSerializer,
                    "refresh": {"type": "string", "description": "JWT refresh token"},
                    "access": {"type": "string", "description": "JWT access token"},
                }
            },
            400: {"description": "Validation error"}
        },
        tags=['Authentication']
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            logger.info(f"New user registered: {user.username}")
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return Response(
                {'error': 'Registration failed'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(generics.RetrieveAPIView):
    """Return the authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get current user profile",
        description="Retrieve the profile of the currently authenticated user.",
        responses={
            200: UserSerializer,
            401: {"description": "Unauthorized"}
        },
        tags=['Users']
    )
    def get_object(self):
        return self.request.user


class LeaderboardView(generics.ListAPIView):
    """Paginated leaderboard view — automatically ordered by '-rating'."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    @extend_schema(
        summary="Get leaderboard",
        description="Retrieve paginated list of users ordered by rating (highest first).",
        parameters=[
            OpenApiParameter(
                name='page',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Page number'
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Number of items per page'
            ),
        ],
        responses={
            200: UserSerializer(many=True),
        },
        tags=['Users']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
