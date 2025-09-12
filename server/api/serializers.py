from typing import override

from rest_framework import serializers

from server.payment.models import Payment, Collect, User


VALIDATION_MESSAGE = (
    'Your donation amount {donation_amount} exceeds the target '
    'amount {target_amount}. You can donate {necessary_amount} '
    'and you will finish this collect!'
)
CLOSED_COLLECT_MESSAGE = (
    'Collect `{title}` is closed! Thanks for your generosity!'
)


class BaseUserSerializer(serializers.ModelSerializer):
    """Base user model serializer with username and email fields."""

    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        abstract = True


class UserCreateSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    @override
    def create(self, validated_data: dict[str, str | int]):
        """Custom method for creating user."""
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )


class UserReadSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class CollectSerializer(serializers.ModelSerializer):
    """Serializer for Collect instances."""
    class Meta:
        model = Collect
        fields = (
            'id',
            'title', 
            'reason',
            'description',
            'target_amount',
            'current_amount',
            'donators_count',
            'created_at',
            'is_finished',
        )
        read_only_fields = (
            'id',
            'current_amount',
            'donators_count',
            'created_at',
            'is_finished',
        )


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment instances."""

    author = UserReadSerializer(source='user')
    collect = CollectSerializer()

    class Meta:
        model = Payment
        fields = ('id', 'amount', 'comment', 'author', 'collect')


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Payment instance."""
    collect_id = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = ('collect_id', 'amount', 'comment')

    @override
    def validate(self, attrs: dict[str, str | int]) -> dict[str, str | int]:
        collect = Collect.objects.get(pk=attrs['collect_id'])
        donation_amount = attrs['amount']
        target_amount = collect.target_amount
        current_amount = collect.current_amount
        if collect.is_finished:
            raise serializers.ValidationError({
                'message': CLOSED_COLLECT_MESSAGE.format(title=collect.title)
            })
        if (
            target_amount is not None
            and current_amount + donation_amount > target_amount
        ):
            raise serializers.ValidationError({
                'amount': VALIDATION_MESSAGE.format(
                    donation_amount=donation_amount,
                    target_amount=target_amount,
                    necessary_amount=target_amount - current_amount,
                )
            })
        return attrs

    @override
    def create(self, validated_data: dict[str, str | int]) -> Payment:
        collect = Collect.objects.get(pk=validated_data.pop('collect_id'))
        payment = Payment.objects.create(collect=collect, **validated_data)
        collect.current_amount += payment.amount
        collect.donators_count += 1
        if collect.target_amount == collect.current_amount:
            collect.is_finished = True
        collect.save()
        return payment
